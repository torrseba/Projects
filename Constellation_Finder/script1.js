//alert('test')
//document.body.innerHTML = '<h1>lol<h1>';
//let input1 =document.getElementsByName('xcoordinate');
//console.log(input1);
//let long = document.getElementById("long");
//let lat = document.getElementById("lat");
//let dat = document.getElementById("date");
const RightA = document.getElementById("RightA");
const Declination = document.getElementById("Declination");
const zoom = document.getElementById("zoom");

//const applicationId ='12bd8c02-b2b9-4cd9-a522-6b3f63234693';
//const applicationSecret = '34fa54cd9605e3ba1185434c1511f29fb26cb1685121b0dd701b47ab1c4be0aec414883f7132593ea135efa5e737507dc21f5baa0f7ace29d94da8c516628c637d21397b9e9f6dba0a24bf602d3a3d1b6a91622895a3847c8373ecd75c7111ee7e9a4f6bc5814f04988176f14a00900f';
//const hash1 = btoa(`${applicationId}:${applicationSecret}`);
const astro = document.getElementById("astro");
const listener = document.getElementById("listener");

let z =0;
let x=0;
let y = 0;
let RA =1;
let dec=1;

//function displayImage(src, width, height) {
//    var img = document.createElement("img");
//    img.src = src;
 //  img.width = width;
//    img.height = height;
//    document.body.appendChild(img);
//   }

function displayImage(src, width, height){ //IMAGE ISSUES NOT UPDATING??????
    document.getElementById("img2").src = src;
    document.getElementById("img2").width = width;
    document.getElementById("img2").height = height;
}


ardu.addEventListener("submit", (e) => {
    e.preventDefault();
    console.log("Fetching Arduino Data...");
    //getImage();
    setInterval(getImage, 5000);
    //clearInterval(loop);
    



});



astro.addEventListener("submit", (e) => {
    e.preventDefault();



    fetch("https://api.astronomyapi.com/api/v2/studio/star-chart", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Basic MTJiZDhjMDItYjJiOS00Y2Q5LWE1MjItNmIzZjYzMjM0NjkzOjM0ZmE1NGNkOTYwNWUzYmExMTg1NDM0YzE1MTFmMjlmYjI2Y2IxNjg1MTIxYjBkZDcwMWI0N2FiMWM0YmUwYWVjNDE0ODgzZjcxMzI1OTNlYTEzNWVmYTVlNzM3NTA3ZGMyMWY1YmFhMGY3YWNlMjlkOTRkYThjNTE2NjI4YzYzN2QyMTM5N2I5ZTlmNmRiYTBhMjRiZjYwMmQzYTNkMWI2YTkxNjIyODk1YTM4NDdjODM3M2VjZDc1YzcxMTFlZTdlOWE0ZjZiYzU4MTRmMDQ5ODgxNzZmMTRhMDA5MDBm",
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
    //console.log(data);
    //console.log(str);
    //console.log(str.data.imageUrl);
    //document.write(data.imageUrl);
    //document.write(str);
    //console.log(long)
    //console.log(longValue);
    //console.log(dateValue);
    //console.log(dateValue)
    console.log(jsonObj.data);
    console.log(jsonObj.data.imageUrl);
    //document.write(str.data.imgUrl);
    //displayImage(jsonObj.data.imageUrl, 700, 700);
    displayImage(jsonObj.data.imageUrl, 600, 600);
    /////////displayImage(str.data, 300, 300);
})
.catch(function(error){
    console.log("Error lolz " + error);
})
}) ;






/*async function getx(){
    let xcord = await fetch("https://io.adafruit.com/api/v2/torrseba/feeds/xaxis", {
        "headers":{
            "x-aio-key":"aio_hSVK99L1uO2OTRZGlgEmPAYwo8W3"
        },
        method:"GET"
    })
    let data = await xcord.json();
    //data.then((value) => x = value)
    let feed = JSON.stringify(data);
    let feedJsonObj = JSON.parse(feed);
    x = feedJsonObj.last_value
    return feedJsonObj.last_value;
}*/


function RAdec(x, y){
    x +=1;
    y+=1;
    RA = x + y;
    dec = x + y;
    console.log("RAAAAAA: ",Number(RA));
    console.log("decccCC: ",Number(dec));
}


function getImage(){ 
    //let longValue = long.value;
    //let latValue = lat.value;
    //let dateValue = dat.value;


    fetch("https://io.adafruit.com/api/v2/torrseba/feeds/x1", {
        "headers":{
            "x-aio-key":"aio_hSVK99L1uO2OTRZGlgEmPAYwo8W3"
        },
        method:"GET"
    }).then(function(response){
        return response.json();
    }).then(function(data){
        var feed = JSON.stringify(data);
        var feedJsonObj = JSON.parse(feed);
        //console.log(feedJsonObj);
        console.log("x: ",feedJsonObj.last_value);
        x = Number(feedJsonObj.last_value);
    })

    fetch("https://io.adafruit.com/api/v2/torrseba/feeds/y1", {
        "headers":{
            "x-aio-key":"aio_hSVK99L1uO2OTRZGlgEmPAYwo8W3"
        },
        method:"GET"
    }).then(function(response){
        return response.json();
    }).then(function(data){
        var feedy = JSON.stringify(data);
        var feedJsonObjy = JSON.parse(feedy);
        //console.log(feedJsonObjy);
        console.log("y: ",feedJsonObjy.last_value);
        y = Number(feedJsonObjy.last_value);
    })

    fetch("https://io.adafruit.com/api/v2/torrseba/feeds/z1", {
        "headers":{
            "x-aio-key":"aio_hSVK99L1uO2OTRZGlgEmPAYwo8W3"
        },
        method:"GET"
    }).then(function(response){
        return response.json();
    }).then(function(data){
        var feedz = JSON.stringify(data);
        var feedJsonObjz = JSON.parse(feedz);
        let today = new Date();
        let hr = today.getHours();
        //let hr = 15;

        //console.log("HR: ",hr);
        let N = (hr + 3) % 24;
        let W = (hr + 9) % 24;
        let S = (hr + 15) % 24;
        let E = (hr + 21) % 24;
        //console.log("South: ",S);

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
                    //RA = hr; 
                    RA = (E + 3) % 24;
                }	
	        }
	        else if(y > .5){
                dec = 40;
                RA = (N + 3) % 24;

            }
            else if(y < -.5){
                dec = 40;
                //RA = hr; 
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
        //console.log("RA is: ", RA);
        //console.log("Dec is :", dec);
        //console.log(feedJsonObjz);
        z = Number(feedJsonObjz.last_value);
        
    })

//call function in fetch to get a RA and DEC value in the .then
    fetch("https://api.astronomyapi.com/api/v2/studio/star-chart", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Basic MTJiZDhjMDItYjJiOS00Y2Q5LWE1MjItNmIzZjYzMjM0NjkzOjM0ZmE1NGNkOTYwNWUzYmExMTg1NDM0YzE1MTFmMjlmYjI2Y2IxNjg1MTIxYjBkZDcwMWI0N2FiMWM0YmUwYWVjNDE0ODgzZjcxMzI1OTNlYTEzNWVmYTVlNzM3NTA3ZGMyMWY1YmFhMGY3YWNlMjlkOTRkYThjNTE2NjI4YzYzN2QyMTM5N2I5ZTlmNmRiYTBhMjRiZjYwMmQzYTNkMWI2YTkxNjIyODk1YTM4NDdjODM3M2VjZDc1YzcxMTFlZTdlOWE0ZjZiYzU4MTRmMDQ5ODgxNzZmMTRhMDA5MDBm",
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
    //console.log(data);
    //console.log(str);
    //console.log(str.data.imageUrl);
    //document.write(data.imageUrl);
    //document.write(str);
    //console.log(long)
    //console.log(longValue);
    //console.log(dateValue);
    console.log(jsonObj.data);
    console.log(jsonObj.data.imageUrl);
    //document.write(str.data.imgUrl);
    //displayImage(jsonObj.data.imageUrl, 700, 700);
    displayImage(jsonObj.data.imageUrl, 600, 600);
    /////////displayImage(str.data, 300, 300);
    })
    .catch(function(error){
    console.log("Error lolz " + error); 
    })

}
