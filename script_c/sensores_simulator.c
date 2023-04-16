#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include "azure-iot-sdk-c/device/transport.h"
#include "azure-iot-sdk-c/iothub_client/inc/iothub_client.h"
#include "azure-iot-sdk-c/iothub_client/inc/iothub_transport_mqtt.h"

const char* connectionString = "{connection_string}";
const char* deviceId = "{device_id}";

float pressure_mean[3] = {1003.3, 1013.3, 1030.3};
float temperature_mean[3] = {15.8, 17.8, 20.8};
float speed_mean[3] = {9.6, 15.6, 19.6};

float temperature_mean;
float pressure_mean;
float air_speed_mean;

float *ptr_temperature_mean;
float *ptr_pressure_mean;
float *ptr_air_speed_mean;

float temperature;
float pressure;
float air_speed;

void set_seed() {
    srand(time(NULL));
}

float generate_pressure_mean(){
   return pressure_mean[rand() % 3];
}

float generate_temperature_mean(){
   return temperature_mean[rand() % 3];
}

float generate_speed_air_mean(){
   return speed_mean[rand() % 3];
}

float simulate_pressure(float *ptr_pressure_mean){
   float min = (*ptr_pressure_mean - 5.0);
   return min + ((float)rand() / (float)RAND_MAX) * 10;
}   

float simulate_temperature(float *ptr_temperature_mean){

   float min = *ptr_temperature_mean - 5.0;
   return min + ((float)rand() / (float)RAND_MAX) * 10;
}   

float simulate_speed_air(float *ptr_speed_mean){
   float min = *ptr_speed_mean - 5.0;
   return min + ((float)rand() / (float)RAND_MAX) * 10;
}   

void send_mensage(char string[10] ,float value){
   sprintf(messagePayload, "%s/%.2f", string, value);
   messageHandle = IoTHubMessage_CreateFromByteArray((const unsigned char*)messagePayload, strlen(messagePayload));
   IoTHubDeviceClient_SendEventAsync(deviceHandle, messageHandle, NULL, NULL);
}

int main() {
   set_seed();
   temperature_mean = generate_temperature_mean();
   pressure_mean = generate_pressure_mean();
   air_speed_mean = generate_speed_air_mean();

   *ptr_temperature_mean = &temperature_mean;
   *ptr_pressure_mean = &pressure_mean;
   *ptr_air_speed_mean = &air_speed_mean;

   IOTHUB_DEVICE_CLIENT_HANDLE deviceHandle;
   IOTHUB_MESSAGE_HANDLE messageHandle;

   deviceHandle = IoTHubDeviceClient_CreateFromConnectionString(connectionString, MQTT_Protocol);
   IoTHubDeviceClient_SetDeviceId(deviceHandle, deviceId);

   int count = 60;
   while (1) {
      if (count == 0){
         temperature_mean = generate_temperature_mean();
         pressure_mean = generate_pressure_mean();
         air_speed_mean = generate_speed_air_mean()
         count = 60
      }

      temperature = simulate_temperature(ptr_temperature_mean);
      pressure = simulate_pressure(ptr_pressure_mean);
      air_speed = simulate_speed_air(ptr_air_speed_mean);
   
      printf("temperature = %.2f\n", temperature);
      printf("pressure = %.2f\n", pressure);
      printf("air_speed = %.2f\n\n", air_speed);

      send_mensage("BPM180", temperature);
      send_mensage("BPM180", pressure);
      send_mensage("anemometro", air_speed);

      count = count - 1;
   }
   return 0;
}

