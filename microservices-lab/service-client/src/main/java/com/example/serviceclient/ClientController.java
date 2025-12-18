package com.example.serviceclient;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.reactive.function.client.WebClient;

@RestController
public class ClientController {

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private CarFeignClient carFeignClient;

    @Autowired
    private WebClient.Builder webClientBuilder;

    @GetMapping("/api/clients/{id}/car/rest")
    public CarResponse getCarRest(@PathVariable Long id) {
        return restTemplate.getForObject("http://service-voiture/api/cars/byClient/" + id, CarResponse.class);
    }

    @GetMapping("/api/clients/{id}/car/feign")
    public CarResponse getCarFeign(@PathVariable Long id) {
        return carFeignClient.getCarByClient(id);
    }

    @GetMapping("/api/clients/{id}/car/webclient")
    public CarResponse getCarWebClient(@PathVariable Long id) {
        return webClientBuilder.build()
                .get()
                .uri("http://service-voiture/api/cars/byClient/" + id)
                .retrieve()
                .bodyToMono(CarResponse.class)
                .block(); // Blocking for synchronous comparison
    }
}
