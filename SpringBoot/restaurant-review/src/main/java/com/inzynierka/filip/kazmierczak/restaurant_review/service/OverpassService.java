package com.inzynierka.filip.kazmierczak.restaurant_review.service;

import com.inzynierka.filip.kazmierczak.restaurant_review.dto.OverpassElement;
import com.inzynierka.filip.kazmierczak.restaurant_review.dto.OverpassResponse;
import com.inzynierka.filip.kazmierczak.restaurant_review.model.Restaurant;
import com.inzynierka.filip.kazmierczak.restaurant_review.repository.RestaurantRepository;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.geo.GeoJsonPoint;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;


@Service
public class OverpassService {

    private static final Logger logger = LoggerFactory.getLogger(OverpassService.class);
    private final WebClient webClient;
    private final RestaurantRepository restaurantRepository;

    // URL do publicznego API Overpass
    private final String OVERPASS_API_URL = "https://overpass-api.de/api/interpreter";

    @Autowired
    public OverpassService(WebClient.Builder webClientBuilder, RestaurantRepository restaurantRepository) {
        this.webClient = webClientBuilder.baseUrl(OVERPASS_API_URL).build();
        this.restaurantRepository = restaurantRepository;
    }

    /**
     * Pobiera restauracje z Overpass API dla danego miasta i zapisuje je do bazy MongoDB.
     * @param cityName Nazwa miasta (np. "Goleniów")
     */
    public Mono<Void> fetchAndSaveRestaurants(String cityName) {
        String query = buildOverpassQuery(cityName);
        logger.info("Wysyłanie zapytania do Overpass API dla miasta: {}", cityName);

        return webClient.post()
                .body(BodyInserters.fromValue(query)) // Wysyłamy zapytanie w ciele POST
                .retrieve() // Odbierz odpowiedź
                .bodyToMono(OverpassResponse.class) // Zmapuj JSON na nasz obiekt DTO
                .flatMap(response -> {
                    logger.info("Otrzymano {} elementów z Overpass API.", response.getElements() != null ? response.getElements().size() : 0);
                    List<Restaurant> restaurantsToSave = convertToRestaurantEntities(response);
                    saveOrUpdateRestaurants(restaurantsToSave);
                    return Mono.empty(); // Zwracamy pusty Mono<Void> po zakończeniu operacji
                })
                .doOnError(error -> logger.error("Błąd podczas komunikacji z Overpass API: {}", error.getMessage()))
                .then(); // Zapewnia, że operacja się zakończy
    }

    // Buduje zapytanie Overpass QL
    private String buildOverpassQuery(String cityName) {
        // Używamy String.format do wstawienia nazwy miasta
        return String.format(
                "[out:json][timeout:25];\n" +
                        "area[\"name\"=\"%s\"]->.searchArea;\n" +
                        "(\n" +
                        "  node[\"amenity\"=\"restaurant\"](area.searchArea);\n" +
                        "  way[\"amenity\"=\"restaurant\"](area.searchArea);\n" +
                        "  relation[\"amenity\"=\"restaurant\"](area.searchArea);\n" +
                        ");\n" +
                        "out geom;", // Zmieniono na 'out geom;' aby dostać współrzędne dla 'way'
                cityName // Wstawia nazwę miasta
        );
    }

    // Konwertuje odpowiedź z Overpass na listę encji Restauracji
    private List<Restaurant> convertToRestaurantEntities(OverpassResponse response) {
        List<Restaurant> restaurants = new ArrayList<>();
        if (response.getElements() == null) {
            return restaurants;
        }

        for (OverpassElement element : response.getElements()) {
            Map<String, String> tags = element.getTags();
            if (tags == null || !tags.containsKey("name")) {
                continue; // Pomiń, jeśli brakuje nazwy
            }

            Double lat = null;
            Double lon = null;

            // Spróbuj pobrać współrzędne
            if ("node".equals(element.getType())) {
                lat = element.getLat();
                lon = element.getLon();
            } else if (element.getCenter() != null) { // Dla 'way' użyj środka
                lat = element.getCenter().getLat();
                lon = element.getCenter().getLon();
            }

            // Stwórz obiekt GeoJsonPoint, jeśli mamy współrzędne
            GeoJsonPoint location = (lat != null && lon != null) ? new GeoJsonPoint(lon, lat) : null;

            // Budujemy encję Restauracji
            Restaurant restaurant = Restaurant.builder()
                    .externalApiId("osm-" + element.getType() + "-" + element.getId()) // Tworzymy unikalne ID
                    .name(tags.get("name"))
                    .location(location)
                    // Możesz dodać mapowanie innych tagów, np. adres
                    // .address(tags.get("addr:street") + " " + tags.get("addr:housenumber"))
                    // Domyślne wartości dla ocen
                    .avgStars(0.0)
                    .avgNlpScores(null) // lub new NlpScores(0,0,0,0)
                    .reviewCount(0)
                    .build();
            restaurants.add(restaurant);
        }
        logger.info("Skonwertowano {} restauracji do zapisu.", restaurants.size());
        return restaurants;
    }

    // Zapisuje lub aktualizuje restauracje w bazie danych
    private void saveOrUpdateRestaurants(List<Restaurant> restaurants) {
        int savedCount = 0;
        int updatedCount = 0;
        for (Restaurant newRestaurant : restaurants) {
            // Sprawdź, czy restauracja z takim externalApiId już istnieje
            restaurantRepository.findByExternalApiId(newRestaurant.getExternalApiId())
                    .ifPresentOrElse(
                            existingRestaurant -> {
                                // Aktualizuj tylko niektóre pola, jeśli potrzeba (np. nazwę, lokalizację)
                                boolean updated = false;
                                if (!existingRestaurant.getName().equals(newRestaurant.getName())) {
                                    existingRestaurant.setName(newRestaurant.getName());
                                    updated = true;
                                }
                                if (newRestaurant.getLocation() != null && !newRestaurant.getLocation().equals(existingRestaurant.getLocation())) {
                                    existingRestaurant.setLocation(newRestaurant.getLocation());
                                    updated = true;
                                }
                                // Możesz dodać aktualizację adresu itp.
                                if(updated) {
                                    restaurantRepository.save(existingRestaurant);
                                    // updatedCount++; // Inkrementacja wewnątrz lambdy może być problematyczna, lepiej logować ID
                                    logger.trace("Zaktualizowano restaurację: {}", existingRestaurant.getExternalApiId());
                                }
                            },
                            () -> {
                                // Jeśli nie istnieje, zapisz nową
                                restaurantRepository.save(newRestaurant);
                                // savedCount++; // Jak wyżej
                                logger.trace("Zapisano nową restaurację: {}", newRestaurant.getExternalApiId());
                            }
                    );
        }
        // Logowanie liczników może wymagać użycia AtomicInteger, jeśli chcesz dokładne liczby
        logger.info("Zakończono zapis/aktualizację restauracji z Overpass API.");
    }
}