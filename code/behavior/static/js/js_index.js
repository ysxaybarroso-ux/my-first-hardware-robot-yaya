function mettreAJourHorloge(){
    let div_horloge = document.querySelector("#horloge")
    let date = new Date()
    div_horloge.innerHTML = date.getDay() +" " + date.getHours().toString().padStart(2, "0") +":" + date.getMinutes().toString().padStart(2, "0") + ":" +date.getSeconds().toString().padStart(2, "0")
    setTimeout(mettreAJourHorloge, 1000)
}




//for the move boy joystick 
let enCours = false
document.getElementById('joystick_patte').addEventListener('mousedown' , function(event) {
    enCours = true;
});
document.getElementById('joystick_patte').addEventListener('mouseup' , function(event) {
    enCours = false;
})

document.addEventListener('mousemove' , function(event){
    if (enCours){
        const zone = document.getElementById('joystick_patte_zone').getBoundingClientRect()
        const centre_x = zone.left +  zone.width / 2
        const centre_y = zone.top +  zone.height /2
        const dx = (event.clientX - centre_x) / (zone.width / 2)
        const dy = (event.clientY - centre_y) / (zone.height / 2);
        fetch('/manual', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({dx: dx, dy: dy})
        });
    }
});

//=====================================for the move cam joystick==========================================

let enCoursCamera = false
document.getElementById('slider_tete').addEventListener('mousedown' , function(event) {
    enCoursCamera = true;
});
document.getElementById('slider_tete').addEventListener('mouseup' , function(event) {
    enCoursCamera = false;
});

document.addEventListener('mousemove' , function(event){
    if (enCoursCamera){
        const zone = document.getElementById('slider_tete_zone').getBoundingClientRect()
        const centre_x = zone.left +  zone.width / 2
        const dx = (event.clientX - centre_x) / (zone.width / 2)
        fetch('/manual_camera', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({dx: dx})
        });
    }
});




document.querySelector('img').addEventListener('click', function(event) {
    fetch('/objectif', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({x: event.offsetX, y: event.offsetY})
    });
})
document.querySelector('img').addEventListener('click', function(event) {
    fetch('/choisir_personne', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({x: event.offsetX, y: event.offsetY})
    });
});



document.querySelector('#shutdown_btn').addEventListener('click', function(event) {
    fetch('/shutdown', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({off: true}) // useless but i prefer (my dev tic i guess)
    });
})

document.querySelector("#onglet-map").addEventListener('click',function(event){
    document.querySelector("#map-preview").style.display = "flex"
    document.querySelector("#camera-preview").style.display = "none"
    document.querySelector("#control-touch").style.display = "none"
       fetch('/state', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({state: "NAVIGATION"}) // useless but i prefer (my dev tic i guess)
    });
})
document.querySelector("#onglet-camera").addEventListener('click',function(event){
    document.querySelector("#map-preview").style.display = "none"
    document.querySelector("#camera-preview").style.display = "flex"
    document.querySelector("#control-touch").style.display = "none"
       fetch('/state', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({state: "FOLLOW"}) // useless but i prefer (my dev tic i guess)
    });
})
document.querySelector("#onglet-manual").addEventListener('click',function(event){
    document.querySelector("#map-preview").style.display = "none"
    document.querySelector("#camera-preview").style.display = "none"
    document.querySelector("#control-touch").style.display = "flex"
       fetch('/state', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({state: "MANUAL"}) // useless but i prefer (my dev tic i guess)
    });
})