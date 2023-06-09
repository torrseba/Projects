
const RightA = document.getElementById("RightA");
const Declination = document.getElementById("Declination");
const zoom = document.getElementById("zoom");

const astro = document.getElementById("astro");
const listener = document.getElementById("listener");

let z =0;
let x=0;
let y = 0;
let RA =1;
let dec=1;
let ASTRO_API_KEY;
let X_AIO_KEY;

document.addEventListener('DOMContentLoaded', function() {
    let key = firebase.database().ref('/ASTRO_KEY')
    key.on('value', snapshot => { 
        ASTRO_API_KEY = snapshot.val();
    });

    let key2 = firebase.database().ref('/X_AIO_KEY')
    key2.on('value', snapshot => { 
        X_AIO_KEY = snapshot.val();
    });

});

function displayImage(src, width, height){ 
    document.getElementById("img2").src = src;
    document.getElementById("img2").width = width;
    document.getElementById("img2").height = height;
}


ardu.addEventListener("submit", (e) => {
    e.preventDefault();
    console.log("Fetching Arduino Data...");
    setInterval(getImage, 5000);
    //clearInterval(loop);
});



astro.addEventListener("submit", (e) => {
    e.preventDefault();

    fetch("https://api.astronomyapi.com/api/v2/studio/star-chart", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": ASTRO_API_KEY,
    "content-type": "application/json;charset=UTF-8",
    "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "sec-gpc": "1",
    "x-requested-with": "XMLHttpRequest",
    "Referer": "http://demo.astronomyapi.com/"
    //"Referrer-Policy": "strict-origin-when-cross-origin"
  },
  method: "POST",
  body:JSON.stringify({style:"inverted",observer:{latitude:Number(1),longitude:Number(1),date:"2023-05-09"},view:{type:"area",parameters:{position:{equatorial:{rightAscension:Number(RightA.value),declination:Number(Declination.value)}},zoom:Number(zoom.value)}}})
    })
    .then(function(response){
    return response.json(); 
    })
    .then(function(data){
    var str = JSON.stringify(data);
    var jsonObj = JSON.parse(str);
    console.log(jsonObj.data);
    console.log(jsonObj.data.imageUrl);
    displayImage(jsonObj.data.imageUrl, 600, 600);
})
.catch(function(error){
    console.log("Error lolz " + error);
})
}) ;


function getImage(){ 

    fetch("https://io.adafruit.com/api/v2/torrseba/feeds/x1", {
        "headers":{
            "x-aio-key": X_AIO_KEY
        },
        method:"GET"
    }).then(function(response){
        return response.json();
    }).then(function(data){
        var feed = JSON.stringify(data);
        var feedJsonObj = JSON.parse(feed);
        console.log("x: ",feedJsonObj.last_value);
        x = Number(feedJsonObj.last_value);
    })

    fetch("https://io.adafruit.com/api/v2/torrseba/feeds/y1", {
        "headers":{
            "x-aio-key": X_AIO_KEY
        },
        method:"GET"
    }).then(function(response){
        return response.json();
    }).then(function(data){
        var feedy = JSON.stringify(data);
        var feedJsonObjy = JSON.parse(feedy);
        console.log("y: ",feedJsonObjy.last_value);
        y = Number(feedJsonObjy.last_value);
    })

    fetch("https://io.adafruit.com/api/v2/torrseba/feeds/z1", {
        "headers":{
            "x-aio-key": X_AIO_KEY
        },
        method:"GET"
    }).then(function(response){
        return response.json();
    }).then(function(data){
        var feedz = JSON.stringify(data);
        var feedJsonObjz = JSON.parse(feedz);
        let today = new Date();
        let hr = today.getHours();

        let N = (hr + 3) % 24;
        let W = (hr + 9) % 24;
        let S = (hr + 15) % 24;
        let E = (hr + 21) % 24;

        if(x <= -.5){

            if((y <= .5) && (y > 0)){
		        dec = 110 + 60*x;
                if(y < .25){
                    RA = N;
                }
                else{
                    RA = (N +  3) % 24;	 
                }
            }
	        else if((y >= -.5) && (y < 0)){
		        dec = 110 + 60*x;
                if(y > -.25){
                    RA = N;
                }
                else{
                    RA = (E + 3) % 24;
                }	
	        }
	        else if(y > .5){
                dec = 40;
                RA = (N + 3) % 24;

            }
            else if(y < -.5){
                dec = 40;
                RA = (E + 3) % 24;
            }
        }

        else if((x < 0) && (x > -.5)){

                if((y <= .5) && (y > 0)){
                    dec = 40 - 100*x;
                    if(y < .25){
                        RA = S;
                    }
                    else{
                        RA = (W + 3) % 24;
                    }
                }
                else if((y >= -.5) && (y < 0)){
                    dec = 40 - 100*x;
                    if(y > -.25){
                        RA = S;
                    }
                    else{
                        RA = (S + 3) % 24;
                    }		
                }
                else if(y > .5){
                    dec = 40;
                    RA = W;
    
                }
                else if(y < -.5){
                    dec = 40;
                    RA = E;
                }
        }	


        else if(x >= 0){
            dec = 40 - 90*x;
            RA = (W + 6 + y*6) % 24;
        }
        console.log("z: ",feedJsonObjz.last_value);
        z = Number(feedJsonObjz.last_value);
        
    })

//call function in fetch to get a RA and DEC value in the .then
    fetch("https://api.astronomyapi.com/api/v2/studio/star-chart", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": ASTRO_API_KEY,
    "content-type": "application/json;charset=UTF-8",
    "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "sec-gpc": "1",
    "x-requested-with": "XMLHttpRequest",
    "Referer": "http://demo.astronomyapi.com/"
    //"Referrer-Policy": "strict-origin-when-cross-origin"
  },
  method: "POST",
  body:JSON.stringify({style:"inverted",observer:{latitude:Number(1),longitude:Number(1),date:"2023-05-09"},view:{type:"area",parameters:{position:{equatorial:{rightAscension:Number(RA),declination:Number(dec)}},zoom:3}}})
    })
    .then(function(response){
    return response.json();
    })
    .then(function(data){
    var str = JSON.stringify(data);
    var jsonObj = JSON.parse(str);
    console.log("RA is: ",Number(RA));
    console.log("dec is: ",Number(dec));
    console.log(jsonObj.data);
    console.log(jsonObj.data.imageUrl);
    displayImage(jsonObj.data.imageUrl, 600, 600);
    })
    .catch(function(error){
    console.log("Error lolz " + error); 
    })

}
