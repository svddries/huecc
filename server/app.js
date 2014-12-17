// --------------------------------------------------------------------------------
//                                  HUE INTERACTION
// --------------------------------------------------------------------------------

var hue = require("node-hue-api");

var displayResult = function(result) {
    console.log(JSON.stringify(result, null, 2));
};

var hostname = "192.168.178.12",
    username = "2416b7e11a8a0f973722b31520319dab",
    api;

api = new hue.HueApi(hostname, username);

// Show light Ids
api.lights().then(displayResult).done();

// --------------------------------------------------------------------------------
//                                  BEAT MEISTER
// --------------------------------------------------------------------------------


var cycle_time;
var t_start;
var timer;
var beat_hues = [ 0, 100, 280, 200]

function set_bpm(bpm) {
    cycle_time = 60.0 / bpm  // in seconds
    t_start = new Date() / 1000;

    if (timer) {
        clearInterval(timer)
    }

    timer = setInterval(function() {
        var t_now = new Date() / 1000;
        var beat = Math.floor((t_now - t_start) / cycle_time) % 4    
        
        console.log("Beat " + (beat + 1))

        // Set light state
        api.setLightState(1, hue.lightState.create().on().hsl(beat_hues[beat], 100, 100).transition(0));
        // api.setLightState(3, hue.lightState.create().on().hsl(beat_hues[beat], 100, 100).transition(0));

    }, cycle_time * 1000);
}

// --------------------------------------------------------------------------------
//                                      SERVER
// --------------------------------------------------------------------------------

var express = require('express')
var bodyParser = require('body-parser')

var app = express()

// parse application/json
app.use(bodyParser.json())

// respond with "Hello World!" on the homepage
app.get('/', function (req, res) {
  res.send('Hello World!');
})

// accept POST request on the homepage
app.post('/', function (req, res) {
  console.log(req.body)

  set_bpm(req.body["bpm"])

  res.send('Got a POST request');
})

// accept PUT request at /user
app.put('/user', function (req, res) {
  res.send('Got a PUT request at /user');
})

// accept DELETE request at /user
app.delete('/user', function (req, res) {
  res.send('Got a DELETE request at /user');
})

var server = app.listen(8000, function () {

  var host = server.address().address
  var port = server.address().port

  console.log('Example app listening at http://%s:%s', host, port)

})

// --------------------------------------------------------------------------------

// set_bpm(124);
