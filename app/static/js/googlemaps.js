
var contentString = "Some useful information is here";

function initialize() {
  var location = new google.maps.LatLng(51.533333, 46);

  var map_options = {
    center: location,
    zoom: 14
  };

  map = new google.maps.Map(document.getElementById('map-container'), map_options);


  var infowindow = new google.maps.InfoWindow({
    content: "Па́мятник Столы́пину — скульптурная композиция, посвященная российскому реформатору, премьер-министру и саратовскому губернатору Петру Столыпину"
  });

  var marker = new google.maps.Marker();

  marker.setPosition(new google.maps.LatLng(51.531667, 46.036389));
  marker.setMap(map);
  marker.setTitle('Памятник Столыпину');
  marker.setLabel('S');

  marker.addListener('click', function() {
    infowindow.open(map, marker);
  });

  var infowindow2 = new google.maps.InfoWindow({
    content: "Памятник Чернышевскому расположен на месте памятника Александру II на площади Чернышевского. Он был построен в 1918 году скульптором П. Ф. Дундуком."
  });

  var marker2 = new google.maps.Marker();

  marker2.setPosition(new google.maps.LatLng(51.529722, 46.035));

  marker2.setMap(map);
  marker2.setTitle('Памятник Чернышевскому');
  marker2.setLabel('C');

  marker2.addListener('click', function() {
    infowindow2.open(map, marker2);
  });

 var infowindow3 = new google.maps.InfoWindow({
   content: "Мемориальный комплекс «Журавли» в парке Победы на Соколовой горе г. Саратова — памятник саратовцам, погибшим в Великой Отечественной войне 1941—1945 гг."
 });
   var marker3 = new google.maps.Marker();
   marker3.setPosition(new google.maps.LatLng(51.544275, 46.049599));
   marker3.setMap(map);
   marker3.setTitle('Мемориальный комплекс «Журавли»');
   marker3.setLabel('C');

   marker3.addListener('click', function() {
   infowindow3.open(map, marker3);
 });

 var infowindow4 = new google.maps.InfoWindow({
   content: "Установка памятника была приурочена к проведению Дней славянской письменности и культуры в Саратове, выбранном столицей проведения торжеств государственного значения"
 });
   var marker4 = new google.maps.Marker();
   marker4.setPosition(new google.maps.LatLng(51.538972, 46.0105));
   marker4.setMap(map);
   marker4.setTitle('Памятник Кириллу и Мефодию');
   marker4.setLabel('K');

   marker4.addListener('click', function() {
   infowindow4.open(map, marker4);
 });

 var infowindow5 = new google.maps.InfoWindow({
   content: "Расположен на площади Революции (Театральной). Cооружён по Постановлению ЦК КПСС и Совета Министров СССР в ознаменование 100-летия со дня рождения"
 });
   var marker5 = new google.maps.Marker();
   marker5.setPosition(new google.maps.LatLng(51.533889, 46.034444));
   marker5.setMap(map);
   marker5.setTitle('Памятник Владимиру Ильичу Ленину');
   marker5.setLabel('L');

   marker5.addListener('click', function() {
   infowindow5.open(map, marker5);
 });


}

function geocodeCity(address, geocoder, map, zoom) {

  geocoder.geocode({'address': address}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      map.setZoom(zoom);
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}


function geocodeMonument(geocoder, resultsMap) {
  var address = document.getElementById('address').value;
  geocoder.geocode({'address': address}, function(results, status) {
   var location = null
    if (status === google.maps.GeocoderStatus.OK) {
      console.log(status)
      resultsMap.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

//google.maps.event.addDomListener(window, 'resize', initialize);
//google.maps.event.addDomListener(window, 'load', initialize);


