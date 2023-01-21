#include "esp_camera.h"
#include <ESP32Servo.h>
#include <WebServer.h>
#include <WiFi.h>
#include <WiFiClient.h>

#define CAMERA_MODEL_AI_THINKER // Has PSRAM
#include "camera_pins.h"

// void startCameraServer();
WebServer server(80);

const char *ssid = "CAM";
const char *password = "CAMERApass";

// Servo
int servoPin = 14;
Servo servo;
void toggle_servo() {
	int position = 0;
	if (position == 0) {
		position = 90;
	} else {
		position = 0;
	}
	servo.write(position);
}

// LED
int ledPin = 33;
bool ledState = false;
void toggle_LED() {
	ledState = !ledState;
	digitalWrite(ledPin, ledState);
}

void handleClient() {
	// Check if the client requested for /TRIGGER
	if (server.hasArg("TRIGGER")) {
		// Call the relevant functions to execute the action
		toggle_LED();
		toggle_servo();
	}
	server.send(200, "text/plain", "TRIGGER received");
}

// Setups
void setup_camera() {
	camera_config_t config;
	config.ledc_channel = LEDC_CHANNEL_0;
	config.ledc_timer = LEDC_TIMER_0;
	config.pin_d0 = Y2_GPIO_NUM;
	config.pin_d1 = Y3_GPIO_NUM;
	config.pin_d2 = Y4_GPIO_NUM;
	config.pin_d3 = Y5_GPIO_NUM;
	config.pin_d4 = Y6_GPIO_NUM;
	config.pin_d5 = Y7_GPIO_NUM;
	config.pin_d6 = Y8_GPIO_NUM;
	config.pin_d7 = Y9_GPIO_NUM;
	config.pin_xclk = XCLK_GPIO_NUM;
	config.pin_pclk = PCLK_GPIO_NUM;
	config.pin_vsync = VSYNC_GPIO_NUM;
	config.pin_href = HREF_GPIO_NUM;
	config.pin_sscb_sda = SIOD_GPIO_NUM;
	config.pin_sscb_scl = SIOC_GPIO_NUM;
	config.pin_pwdn = PWDN_GPIO_NUM;
	config.pin_reset = RESET_GPIO_NUM;
	config.xclk_freq_hz = 20000000;
	config.frame_size = FRAMESIZE_UXGA;
	config.pixel_format = PIXFORMAT_JPEG; // for streaming
	// config.pixel_format = PIXFORMAT_RGB565; // for face detection/recognition
	config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
	config.fb_location = CAMERA_FB_IN_PSRAM;
	config.jpeg_quality = 12;
	config.fb_count = 1;

	// if PSRAM IC present, init with UXGA resolution and higher JPEG quality
	//                      for larger pre-allocated frame buffer.
	if (config.pixel_format == PIXFORMAT_JPEG) {
		if (psramFound()) {
			config.jpeg_quality = 10;
			config.fb_count = 2;
			config.grab_mode = CAMERA_GRAB_LATEST;
		} else {
			// Limit the frame size when PSRAM is not available
			config.frame_size = FRAMESIZE_SVGA;
			config.fb_location = CAMERA_FB_IN_DRAM;
		}
	} else {
		// Best option for face detection/recognition
		config.frame_size = FRAMESIZE_240X240;
#if CONFIG_IDF_TARGET_ESP32S3
		config.fb_count = 2;
#endif
	}

#if defined(CAMERA_MODEL_ESP_EYE)
	pinMode(13, INPUT_PULLUP);
	pinMode(14, INPUT_PULLUP);
#endif

	// camera init
	esp_err_t err = esp_camera_init(&config);
	if (err != ESP_OK) {
		Serial.printf("Camera init failed with error 0x%x", err);
		return;
	}

	sensor_t *s = esp_camera_sensor_get();
	// initial sensors are flipped vertically and colors are a bit saturated
	if (s->id.PID == OV3660_PID) {
		s->set_vflip(s, 1);		  // flip it back
		s->set_brightness(s, 1);  // up the brightness just a bit
		s->set_saturation(s, -2); // lower the saturation
	}
	// drop down frame size for higher initial frame rate
	if (config.pixel_format == PIXFORMAT_JPEG) {
		s->set_framesize(s, FRAMESIZE_QVGA); // change to higher resolution https://randomnerdtutorials.com/esp32-cam-ov2640-camera-settings/
	}

#if defined(CAMERA_MODEL_M5STACK_WIDE) || defined(CAMERA_MODEL_M5STACK_ESP32CAM)
	s->set_vflip(s, 1);
	s->set_hmirror(s, 1);
#endif

#if defined(CAMERA_MODEL_ESP32S3_EYE)
	s->set_vflip(s, 1);
#endif
}

void setup_webserver() {
	// Start the server
	server.begin();
	// Set the function to handle client requests
	server.on("/", HTTP_GET, handleClient);
	// Attach the camera
	server.on("/capture", HTTP_GET, []() {
		camera_fb_t *fb = NULL;
		fb = esp_camera_fb_get();
		if (!fb) {
			Serial.println("Camera capture failed");
			return;
		}
		// Send the framebuffer to the client
		server.sendHeader("Content-Type", "image/jpeg");
		server.sendHeader("Content-Length", String(fb->len));
		server.send_P(200, "image/jpeg", (const char *)fb->buf, fb->len);
		esp_camera_fb_return(fb);
	});
	// Handle client connections
	server.begin();
	Serial.println("Web server started");
}

void setup_socket() {
	WiFiServer server(80);
	server.begin();
	Serial.println("Socket server started");

	// Wait for incomming connections
	WiFiClient client = server.available();
	if (!client)
		return;

	// Wait for data from the client
	while (client.connected()) {
		if (client.available()) {
			String req = client.readStringUntil('\n');
			Serial.println(req);

			// If the client sends TRIGGER, call the relevant function
			if (req.indexOf("TRIGGER") != -1) {
				toggle_LED();
				toggle_servo();
			}
		}
	}
	client.stop();
	Serial.println("Client disconnected");
}

void setup() {
	Serial.begin(115200);
	Serial.setDebugOutput(true);
	Serial.println();

	// WiFi
	WiFi.begin(ssid, password);
	WiFi.setSleep(false);

	// Setups
	setup_camera();
	setup_webserver();
	setup_socket();

	// Servo
	servo.attach(servoPin);
	//  startCameraServer();
}

void loop() {
	server.handleClient();
}