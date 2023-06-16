$(function () {

  var tavt;
  var iavt = 0;
  var isong = 0;
  var listsong = [];
  var newItem;

  loadavt();  
  onload();
  randomItem();
  $(".poca-btn").on('click', function (e) {
    for (var i = 0; i < 4; i++, isong++) {
      if (isong < listsong.length) {
        newItem = createMoreItem();
        $("#poca-container").append(newItem);
        $("#poca-container").addClass("poca-music-player");
      }
    }
    fixPocaContainerHeight();

  });
  function randomItem(){
    if (listsong.length <  Treading.length) {
      var i = Math.floor(Math.random() * Treading.length);
      var flag = true;
      for(k in listsong) if(listsong[k] == i) flag = false;
        if(flag){
         listsong.push(i);
        }
      randomItem();
    }
    else{
      for (var i = 0; i < 6; i++, isong++) {
        newItem = createMoreItem();
        $("#poca-container").append(newItem);
        $("#poca-container").audioPlayer();
      }
      fixPocaContainerHeight();
    }
  }

  function createMoreItem(){
    
    var item ="";
    item= "<div class='col-12 col-md-6' id='"+Treading[listsong[isong]]["type"]+"'>";
    item+= "<!-- Welcome Music Area -->";
    item+="  <div class='poca-music-area style-2 d-flex align-items-center flex-wrap'>";
    item+="    <div class='poca-music-thumbnail'>";
    item+="      <img src='data/img/"+Treading[listsong[isong]]["img"]+"' alt=''>";
    item+="    </div>";
    item+="    <div class='poca-music-content text-center'>";
    item+="      <span class='music-published-date mb-2'>"+Treading[listsong[isong]]["type"]+"</span>";
    item+="      <h2>"+Treading[listsong[isong]]["song"]+"</h2>";
    item+="      <div class='music-meta-data'>";
    item+="        <p>By <a href='#!' class='music-author'>Admin</a> | <a href='#!' class='music-author'>"+Treading[listsong[isong]]["artist"]+"</a></p>";
    item+="      </div>";
    item+="        <!-- Music Player -->";
    item+="        <div class='poca-music-player'>";
    item+="          <audio preload='auto' controls>";
    item+="            <source src='data/audio/"+Treading[listsong[isong]]["dir"]+"'>";
    item+="          </audio>";
    item+="        </div>";
    item+="      <!-- Likes, Share & Download -->";
    item+="      <div class='likes-share-download d-flex align-items-center justify-content-between'>";
    item+="        <a href='#!'><i class='fa fa-heart' aria-hidden='true'></i> Like (29)</a>";
    item+="        <div>";
    item+="          <a href='#!' class='mr-4'><i class='fa fa-share-alt' aria-hidden='true'></i> Share(04)</a>";
    item+="          <a href='#!'><i class='fa fa-download' aria-hidden='true'></i> Download (12)</a>";
    item+="        </div>";
    item+="      </div>";
    item+="    </div>";
    item+="  </div>  ";
    item+="</div>";
    return item;
  }

  function fixPocaContainerHeight(){
    var x = Math.ceil($("#poca-container").children().length / 2);
    $("#poca-container").height(x * 840 + 200);
  }

  function onload(){
    selectnv("#nv"+iavt);
    tavt = setInterval(nextnv, 8000);
  }

  function selectnv(idnv){
    iavt = idnv[idnv.length -1];
    $(".selected").removeClass('selected');

    loadnv($(idnv).attr("name"));
    $(idnv).addClass('selected');
  }

  function loadnv(tennv){
    $("#detail").empty();
    var avtUrl = 'data/img/avt_'+tennv+'.jpg';

    $("#avtContainer").stop().fadeTo(100, 0.0,function(){
      $("#avatar").attr({src: avtUrl});
      $("#avtContainer").stop().fadeTo(500, 1.0);
    });
    
    $('#foward a').attr( 'href', 'Detail.html?name='+tennv);

    $("#detail").stop().slideUp(function(){
      for(var nv in bgr){
        list = bgr[nv];
        if(list["Name"] == tennv){
          for(var k in list) {
            //console.log(k, list[k]);
            $("#detail").append("<span class='key'>"+k+":</span>");
            $("#detail").append("<span class='value'>"+list[k]+"</span><br>");
          }
        }
      }
    loadUrl();
    $("#detail").stop().slideDown();
    });
  }

  function loadUrl() {
    $(".value a").attr('href', function () {
        return $(this).attr('href')+'.html?name='+$(this).text();
    });
  }

  function loadavt(){
    var listnv = [];
    chonnv(listnv);
    for (var i = 0; i < 9; i++) {
      $("#nv"+i).attr({src: 'data/img/avt_'+listnv[i]+'.jpg', name: listnv[i]});
    };
  }

  function nextnv(){
    iavt++;
    if(iavt>8) iavt = 0;
    selectnv("#nv"+iavt);
  }

  function chonnv(listnv){
    if(listnv.length<9){
      var i = Math.floor(Math.random() * bgr.length);
      var flag = true;
      for(k in listnv) if(listnv[k] == i) flag = false;
      if(flag)
        listnv.push(i);
      chonnv(listnv);
    }else{
      getsrc(listnv);
    }
  }

  function getsrc(listnv){
    var src;
    for(k in listnv){
      listnv[k] = (bgr[listnv[k]]["Name"]);
    }
  }

  $(".small-avt").on("click", function(){
    selectnv("#"+$(this).attr("id"));
    clearInterval(tavt);
    tavt = setInterval(nextnv, 15000);
  });

});

var audioPlayer = document.querySelector('.green-audio-player');
var playPause = audioPlayer.querySelector('#playPause');
var playpauseBtn = audioPlayer.querySelector('.play-pause-btn');
var loading = audioPlayer.querySelector('.loading');
var progress = audioPlayer.querySelector('.progress');
var sliders = audioPlayer.querySelectorAll('.slider');
var volumeBtn = audioPlayer.querySelector('.volume-btn');
var volumeControls = audioPlayer.querySelector('.volume-controls');
var volumeProgress = volumeControls.querySelector('.slider .progress');
var player = audioPlayer.querySelector('audio');
var currentTime = audioPlayer.querySelector('.current-time');
var totalTime = audioPlayer.querySelector('.total-time');
var speaker = audioPlayer.querySelector('#speaker');

var draggableClasses = ['pin'];
var currentlyDragged = null;

window.addEventListener('mousedown', function(event) {
  
  if(!isDraggable(event.target)) return false;
  
  currentlyDragged = event.target;
  let handleMethod = currentlyDragged.dataset.method;
  
  this.addEventListener('mousemove', window[handleMethod], false);

  window.addEventListener('mouseup', () => {
    currentlyDragged = false;
    window.removeEventListener('mousemove', window[handleMethod], false);
  }, false);  
});

playpauseBtn.addEventListener('click', togglePlay);
player.addEventListener('timeupdate', updateProgress);
player.addEventListener('volumechange', updateVolume);
player.addEventListener('loadedmetadata', () => {
  totalTime.textContent = formatTime(player.duration);
});
player.addEventListener('canplay', makePlay);
player.addEventListener('ended', function(){
  playPause.attributes.d.value = "M18 12L0 24V0";
  player.currentTime = 0;
});

volumeBtn.addEventListener('click', () => {
  volumeBtn.classList.toggle('open');
  volumeControls.classList.toggle('hidden');
})

window.addEventListener('resize', directionAware);

sliders.forEach(slider => {
  let pin = slider.querySelector('.pin');
  slider.addEventListener('click', window[pin.dataset.method]);
});

directionAware();

function isDraggable(el) {
  let canDrag = false;
  let classes = Array.from(el.classList);
  draggableClasses.forEach(draggable => {
    if(classes.indexOf(draggable) !== -1)
      canDrag = true;
  })
  return canDrag;
}

function inRange(event) {
  let rangeBox = getRangeBox(event);
  let rect = rangeBox.getBoundingClientRect();
  let direction = rangeBox.dataset.direction;
  if(direction == 'horizontal') {
    var min = rangeBox.offsetLeft;
    var max = min + rangeBox.offsetWidth;   
    if(event.clientX < min || event.clientX > max) return false;
  } else {
    var min = rect.top;
    var max = min + rangeBox.offsetHeight; 
    if(event.clientY < min || event.clientY > max) return false;  
  }
  return true;
}

function updateProgress() {
  var current = player.currentTime;
  var percent = (current / player.duration) * 100;
  progress.style.width = percent + '%';
  
  currentTime.textContent = formatTime(current);
}

function updateVolume() {
  volumeProgress.style.height = player.volume * 100 + '%';
  if(player.volume >= 0.5) {
    speaker.attributes.d.value = 'M14.667 0v2.747c3.853 1.146 6.666 4.72 6.666 8.946 0 4.227-2.813 7.787-6.666 8.934v2.76C20 22.173 24 17.4 24 11.693 24 5.987 20 1.213 14.667 0zM18 11.693c0-2.36-1.333-4.386-3.333-5.373v10.707c2-.947 3.333-2.987 3.333-5.334zm-18-4v8h5.333L12 22.36V1.027L5.333 7.693H0z';  
  } else if(player.volume < 0.5 && player.volume > 0.05) {
    speaker.attributes.d.value = 'M0 7.667v8h5.333L12 22.333V1L5.333 7.667M17.333 11.373C17.333 9.013 16 6.987 14 6v10.707c2-.947 3.333-2.987 3.333-5.334z';
  } else if(player.volume <= 0.05) {
    speaker.attributes.d.value = 'M0 7.667v8h5.333L12 22.333V1L5.333 7.667';
  }
}

function getRangeBox(event) {
  let rangeBox = event.target;
  let el = currentlyDragged;
  if(event.type == 'click' && isDraggable(event.target)) {
    rangeBox = event.target.parentElement.parentElement;
  }
  if(event.type == 'mousemove') {
    rangeBox = el.parentElement.parentElement;
  }
  return rangeBox;
}

function getCoefficient(event) {
  let slider = getRangeBox(event);
  let rect = slider.getBoundingClientRect();
  let K = 0;
  if(slider.dataset.direction == 'horizontal') {
    
    let offsetX = event.clientX - slider.offsetLeft;
    let width = slider.clientWidth;
    K = offsetX / width;    
    
  } else if(slider.dataset.direction == 'vertical') {
    
    let height = slider.clientHeight;
    var offsetY = event.clientY - rect.top;
    K = 1 - offsetY / height;
    
  }
  return K;
}

function rewind(event) {
  if(inRange(event)) {
    player.currentTime = player.duration * getCoefficient(event);
  }
}

function changeVolume(event) {
  if(inRange(event)) {
    player.volume = getCoefficient(event);
  }
}

function formatTime(time) {
  var min = Math.floor(time / 60);
  var sec = Math.floor(time % 60);
  return min + ':' + ((sec<10) ? ('0' + sec) : sec);
}

function togglePlay() {
  if(player.paused) {
    playPause.attributes.d.value = "M0 0h6v24H0zM12 0h6v24h-6z";
    player.play();
  } else {
    playPause.attributes.d.value = "M18 12L0 24V0";
    player.pause();
  }  
}

function makePlay() {
  playpauseBtn.style.display = 'block';
  loading.style.display = 'none';
}

function directionAware() {
  if(window.innerHeight < 250) {
    volumeControls.style.bottom = '-54px';
    volumeControls.style.left = '54px';
  } else if(audioPlayer.offsetTop < 154) {
    volumeControls.style.bottom = '-164px';
    volumeControls.style.left = '-3px';
  } else {
    volumeControls.style.bottom = '52px';
    volumeControls.style.left = '-3px';
  }
}