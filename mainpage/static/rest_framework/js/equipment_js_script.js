var equip_app=angular.module('equip_app',['ngRoute'])

var postJson=function(link,$http,equip,quantity,approved,delivered)
{
    var request=$http({
        method:"post",
        url: link,
        //transformRequest:
        data:
            {
            "equipment": {
        "equip": equip,
        "quantity": quantity,
        "approved_by_manager": approved,
                "delivered": delivered
    }
}
    })
}

var putJson=function(link,$http,equip,quantity,approved,delivered)
{
    var request=$http({
        method:"put",
        url: link,
        //transformRequest:
        data:
            {
            "equipment": {
        "equip": equip,
        "quantity": quantity,
        "approved_by_manager": approved,
                "delivered": delivered
    }
}
    })
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


equip_app.run(function($http) {
  $http.defaults.xsrfCookieName = 'csrftoken';
$http.defaults.xsrfHeaderName = 'X-CSRFToken';
});


equip_app.controller('Equipment_controller', function ($scope, $http, )
    {
        $scope.not_logined_warning="asdada"
        $scope.id_input=0
        $scope.equip_input="Канцелярия"
        $scope.quantity_input=1
        $scope.approved_by_manager_input=false
        $scope.delivered_input=false

        $scope.GetMethod = function (ll) {
            console.log(ll)
            getJSON('https://trsis-labs.azurewebsites.net/equipment_api/', function (err,data) {
                if (err!=null)
                {
                    alert('something went wrong'+ err);
                }
                else
                {
                    console.log(data["equipment"])
                    $scope.pos=data["equipment"]
                }
            });

        }

        $scope.PostMethod = function ()
        {

            postJson('https://trsis-labs.azurewebsites.net/equipment_api/', $http, $scope.equip_input, $scope.quantity_input, $scope.approved_by_manager_input, $scope.delivered_input)
            console.log('posted (at least i tried)')
        }

        $scope.DeleteAll = function()
        {
            $http.delete('https://trsis-labs.azurewebsites.net/equipment_api/')
        }

        $scope.DeleteByPK = function (id)
        {
            //console.log(id)
            var url = 'https://trsis-labs.azurewebsites.net/equipment_api/'+ id.toString()
            //console.log(url)
            $http.delete(url)
        }

        $scope.PutByPK = function (id)
        {
            var url = 'https://trsis-labs.azurewebsites.net/equipment_api/'+ id.toString()
            putJson(url, $http, $scope.equip_input, $scope.quantity_input, $scope.approved_by_manager_input, $scope.delivered_input)
        }

    }
)