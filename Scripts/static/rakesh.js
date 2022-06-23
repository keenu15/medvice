var video1 = document.getElementById("myVideo");
var videoplay = document.getElementById("videodiv");
var showContact = document.getElementById("show-contact");
var showC = document.getElementById("showC");
showContact.style.display="none"
function videochange()
{var video=["video/video6.mp4","video/video5.mp4","video/video4.mp4","video/video3.mp4","video/video2.mp4","video/video1.mp4"]
let index= Math.floor((Math.random()*video.length));
console.log(video[index]);
document.getElementById("src").setAttribute("src",video[index]);
video1.load();
};

function showContactme()
{
if(showContact.style.display==="none")
{
showContact.style.display="block";
}
else
{
  showContact.style.display="none";
}
};