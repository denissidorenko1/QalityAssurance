var app=angular.module('app',[])

var postJson=function(link,$http,title,bio,id)
{
    var request=$http({
        method:"post",
        url: link,
        //transformRequest:
        data:
            {
            "contributors": {
        "title": title,
        "bio": bio,
        "contributor_id": id
    }
}

    })
    console.log("post")
}


var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

app.controller('MainCtrl', function($scope, $http)
    {
        $scope.title_input="Дефолтное ФИО"
        $scope.bio_input="Дефолтное БИО"
        $scope.contributor_id_input=0
        $scope.GetC = function ()
        {
            getJSON('https://trsis-labs.azurewebsites.net/about/', function(err, data) {
            if (err !== null)
            {
                 alert('Something went wrong: ' + err);
            }
            else {
                console.log(data["contributors"])
                $scope.val=data["contributors"]
                }
            });

        }

        $scope.Post=function ()
        {
            postJson('https://trsis-labs.azurewebsites.net/about/',$http, $scope.title_input,$scope.bio_input, $scope.contributor_id_input);
            console.log("tried posting")
        }

        $scope.DeleteAll=function ()
        {
            $http.delete('https://trsis-labs.azurewebsites.net/about/')
        }
    }
)