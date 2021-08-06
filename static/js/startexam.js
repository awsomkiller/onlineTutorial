var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

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
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
      // add an "invalid" class to the field:
      document.getElementsByClassName("step")[currentTab].className += " invalid";
      // and set the current valid status to false
      valid = true;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
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




    (function () {

      var timeElement, eventTime, currentTime, duration, interval, intervalId;
    
      interval = 1000; // 1 second
      startTime = $('#startTime').val();
      endTime = $('#endTime').val();
      // get time element
      timeElement = document.querySelector("time");
      // calculate difference between two times
      eventTime = moment.tz(endTime, "Asia/Jakarta");
      // based on time set in user's computer time / OS
      currentTime = moment.tz(startTime, "Asia/Jakarta");
      // get duration between two times
      duration = moment.duration(eventTime.diff(currentTime));
    
      // loop to countdown every 1 second
      setInterval(function() {
        // get updated duration
        duration = moment.duration(duration - interval, 'milliseconds');
    
        // if duration is >= 0
        if (duration.asSeconds() <= 0) {
          clearInterval(intervalId);
          // hide the countdown element
          $('#msform').submit();
          timeElement.classList.add("hidden");
        } else {
          // otherwise, show the updated countdown
          timeElement.innerText =  duration.hours() + ":" + duration.minutes() + ":" + duration.seconds()
        }
      }, interval);
    
    }());

    var NoQuestion = document.querySelectorAll('.tab');

    $('#progress').append('<button id="progressbtn1" type="button" class="step btn btn-primary btn-sm border">1</button>');
    for (let index = 2; index <= NoQuestion.length; index++) {
      $('#progress').append('<button id="progressbtn'+index+'" type="button" class="step btn btn-light btn-sm border">'+index+'</button>');
    }