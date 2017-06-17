var app = angular.module('RegisterApp', ['ngMaterial', 'ngMessages']);

app.config(function($httpProvider, $mdThemingProvider){
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $mdThemingProvider.theme('registerTheme')
    .primaryPalette('blue')
    .accentPalette('pink')
    .warnPalette('pink');
  $mdThemingProvider.setDefaultTheme('registerTheme');
});



app.run(function(){
  console.log("App is runing!");
  //This will ask permission so that's not a good
  /*
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
      };
      console.log(pos);
    });
  }
  */
});

app.factory('googleMapService', function($http, $q) {
  return {
    getAutoCompleteResult: function(searchText) {
      var deferred = $q.defer();
      var service = new google.maps.places.AutocompleteService();
      brooklynLatLng = new google.maps.LatLng({lat: 40.6782, lng: -73.9442});
      service.getQueryPredictions({ input: searchText, location: brooklynLatLng, radius: 0 }, function(predictions, status) {
        if (status == google.maps.places.PlacesServiceStatus.OK) {
          deferred.resolve(predictions);
        } else if (status == google.maps.places.PlacesServiceStatus.ZERO_RESULTS) {
          deferred.resolve([]);
        }
        else {
          deferred.reject([]);
        }
      });
      return deferred.promise;
    },
    getAddressMapImage: function(selectedItem) {
      var deferred = $q.defer();
      console.log(selectedItem);
      var BACKEND_URL = "https://maps.googleapis.com/maps/api/staticmap?center="+selectedItem.description+"&zoom=15&size=600x150&scale=1&markers=color:purple%7Clabel:S%7C11211&key=AIzaSyBpipxLAeJ0Kp_AMberNgzShneoXd0V-Dg";
      deferred.resolve(BACKEND_URL);
      return deferred.promise;
    }
  }
});

app.controller('AppCtrl', function($scope, $timeout, googleMapService) {
  var self = this;
  var BACKEND_URL = "/place/autocomplete/";

  $scope.autoCompleteResults = null;
  $scope.selectedItemImageURL = null;

  self.businessCategories = []

  self.googleMapService = googleMapService;

  self.loadBusinessCategories = function() {
    // Use timeout to simulate a 1200ms request.
    return $timeout(function() {
      self.businessCategories = [{label:'Cocktail Bar', value:3}, {label:'Restaurant', value:1}, {label:'Clothing Store', value:2}];
    }, 1200);
  };

  $scope.query = function(searchText) {
    if (searchText != "") {
      //Commented this to use async progress bar on autocomplete
      /*
      var promise = googleMapService.getAutoCompleteResult(searchText);
      promise.then(
        function(data){
          $scope.autoCompleteResults = data;
        },
        function(){
          console.log("Something went worng!");
        }
      );
      */
    } else {
      $scope.autoCompleteResults = null;
      $scope.selectedItemImageURL = null;
    }
  };

  $scope.getMapImage = function(selectedItem) {
    if (selectedItem !== null) {
      var promise = googleMapService.getAddressMapImage(selectedItem);
      promise.then(
        function(data){
          $scope.selectedItemImageURL = data;
        }
      );
    }
  };
});
