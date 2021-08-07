// function CloseWindow(){
//   alert("Thank you for visiting W3Schools!");
// }
//$(window).unload( function () { alert("Bye now!"); } );


// function requestFullScreen(element) {
//   // Supports most browsers and their versions.
//   var requestMethod = element.requestFullScreen || element.webkitRequestFullScreen || element.mozRequestFullScreen || element.msRequestFullScreen;

//   if (requestMethod) { // Native full screen.
//       requestMethod.call(element);
//   } else if (typeof window.ActiveXObject !== "undefined") { // Older IE.
//       var wscript = new ActiveXObject("WScript.Shell");
//       if (wscript !== null) {
//           wscript.SendKeys("{F11}");
//       }
//   }
// }

// var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
// if(isChrome){
  $('#overlay').css('display','none');
//}
//console.log(isChrome);


navigator.keyboard.lock();

function fullscreen() {
  var isInFullScreen = (document.fullscreenElement && document.fullscreenElement !== null) ||
      (document.webkitFullscreenElement && document.webkitFullscreenElement !== null) ||
      (document.mozFullScreenElement && document.mozFullScreenElement !== null) ||
      (document.msFullscreenElement && document.msFullscreenElement !== null);

  var docElm = document.documentElement;
  if (!isInFullScreen) {
      if (docElm.requestFullscreen) {
          docElm.requestFullscreen();
      } else if (docElm.mozRequestFullScreen) {
          docElm.mozRequestFullScreen();
      } else if (docElm.webkitRequestFullScreen) {
          docElm.webkitRequestFullScreen();
      } else if (docElm.msRequestFullscreen) {
          docElm.msRequestFullscreen();
      }
      
      if (docElm.exitFullscreen) {
        //document.exitFullscreen();
          alert('close');
      } else if (docElm.webkitExitFullscreen) {
          //document.webkitExitFullscreen();
          alert('close');
      } else if (docElm.mozCancelFullScreen) {
          //document.mozCancelFullScreen();
      } else if (docElm.msExitFullscreen) {
          //document.msExitFullscreen();
          alert('close');
      }
  }
      
}


var elem = document.body; // Make the body go full screen.
//fullscreen(elem);



var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function opentab(numb){
  var my,tabu = document.getElementsByClassName("tab");
  fixStepIndicator(numb);
  for (var my = 0; my <= tabu.length; my++){
      if(tabu[my].attributes.style.nodeValue == "display: block;"){
     //   console.log(`ok ${my} block`);
        tabu[my].style.display = "none";
        tabu[numb].style.display = "block";
      }
   // console.log(`ok ${my} block`);
  }
  
  
  
}

function showTab(n) {
  // This function will display the specified tab of the form...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  //... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  //... and run a function that will display the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form...
  if (currentTab >= x.length) {
    // ... the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function markflag(){
  flag = currentTab;
  localStorage.setItem("flag", currentTab);
  document.getElementsByClassName("step")[flag].className += " flag";
}


function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  //y = x[currentTab].getElementsByClassName("quest_type");
  //z = [currentTab].getElementsByClassName("question");
  y = document.querySelectorAll('.quest_type')[currentTab];
  if(y.value == 'normal_mcq'){
    var normal_mcq_checbox = document.getElementsByName('normal_mcq');
    var formValid = false;
    
    var i = 0;
    while (!formValid && i < normal_mcq_checbox.length) {
        if (normal_mcq_checbox[i].checked) formValid = true;
        i++;      
    }

    if (!formValid){
      document.getElementsByClassName("step")[currentTab].className += " invalid";
    }
  
  }else if(y.value == 'multiselect'){
    var normal_mcq_checbox = document.getElementsByName('multiselectoption');
    var formValid = false;
    
    var i = 0;
    while (!formValid && i < normal_mcq_checbox.length) {
        if (normal_mcq_checbox[i].checked) formValid = true;
        i++;      
    }

    if (!formValid){
      document.getElementsByClassName("step")[currentTab].className += " invalid";
    }else{
      document.getElementsByClassName("step")[currentTab].className.replace(" invalid", "");
    }
  }else if(y.value == 'qa_question'){
    var textarea = x[currentTab].getElementsByTagName("qa_question");
    var formValid = false;
    if(textarea.value == ''){
      formValid = true;
    }

    if(!formValid){
      document.getElementsByClassName("step")[currentTab].className += " invalid";
    }else{
      document.getElementsByClassName("step")[currentTab].className.replace(" invalid", "");
    }

  }
  
  valid = true;
  if (formValid) {
    
    // if(document.getElementsByClassName("step")[currentTab].classList.contains('invalid')) {
    //   document.getElementsByClassName("step")[currentTab].className.replace(" invalid", "");
    // }
    

    document.getElementsByClassName("step")[currentTab].className += " finish";

  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class on the current step:
  x[n].className += " active";
}


Timer();

function Timer() {
  var deadline = new Date("Aug. 7, 2021, 00:30:00");
  var newDateObj = new Date();
  newDateObj.setTime(deadline.getTime() + ($('#durations').val() * 60 * 1000));
  //console.log(newDateObj);
  var x = setInterval(function() {
  Startexam = deadline.getTime() <= new Date().getTime();
  if(Startexam){
  var now = new Date().getTime();
  var t = newDateObj - now;
  var days = Math.floor(t / (1000 * 60 * 60 * 24));
  var hours = Math.floor((t%(1000 * 60 * 60 * 24))/(1000 * 60 * 60));
  var minutes = Math.floor((t % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((t % (1000 * 60)) / 1000);
  document.querySelector("time").innerHTML = hours + ":" + minutes + ":" + seconds;
      if (t < 0) {
          clearInterval(x);
          $('#ms').submit();
          navigator.keyboard.unlock();
          document.querySelector("time").innerHTML = 0 + ":" + 0 + ":" + 0;
      }
      }else{
        console.log("Not started yet");
  }
  }, 1000);
}



    var NoQuestion = document.querySelectorAll('.tab');

    $('#progress').append('<button id="progressbtn1" type="button" class="step btn btn-light btn-sm border active" onclick="opentab(0)">1</button>');
    for (let index = 2; index < NoQuestion.length; index++) {
      forClickableIndicator = index -1;
      //NoQuestion.splice(index, 1);
      $('#progress').append(`<button id="progressbtn${index}" type="button" class="step btn btn-light btn-sm border" onclick="opentab(${forClickableIndicator})">${index}</button>`);
    }