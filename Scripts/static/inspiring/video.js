var video1 = document.getElementById("myVideo");
var videoplay = document.getElementById("videodiv");
document.getElementById('but').addEventListener('click',
function() {
var videos=["videos/video4.mp4","videos/video5.mp4","videos/video3.mp4","videos/video2.mp4","videos/video1.mp4"]
let index= Math.floor((Math.random()*videos.length));
console.log(videos[index]);
document.getElementById("src").setAttribute("src",videos[index]);
video1.load();
}
);
