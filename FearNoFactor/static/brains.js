  var BASIC_LIMIT = 144
  var ADVANCED_LIMIT = 300

  // Numpad functionality

  function displayLeftNumpad() {
    document.getElementById('right_nums').style.display = 'none';
    document.getElementById('left_nums').style.display = 'block';
    document.getElementById('focus-right-numpad').className = 'btn btn-primary numpadbutton';
    document.getElementById('focus-left-numpad').className = 'btn btn-outline-primary numpadbutton';
  }

  function displayRightNumpad() {
    document.getElementById('left_nums').style.display = 'none';
    document.getElementById('right_nums').style.display = 'block';
    document.getElementById('focus-left-numpad').className = 'btn btn-primary numpadbutton';
    document.getElementById('focus-right-numpad').className = 'btn btn-outline-primary numpadbutton';
  }

  function numPress(numpad, number) {
    // console.log(numpad);
    // console.log(number);
    if (number != "-1") {
      addDigit(numpad, number);
    } else {
      removeDigit(numpad);
    }
  }

  function addDigit(factorField, digit) {
    factorID = "factor" + factorField;
    // console.log(factorID);

    factorFields = document.getElementsByClassName(factorID);
    contents = factorFields[0].innerHTML;
    if (contents.length >= 3) {
      return
    }
    for (var i = 0; i < factorFields.length; i++) {
        factorFields[i].innerHTML = contents + digit
    }

  }

  function removeDigit(factorField) {
    factorID = "factor" + factorField;
    // console.log(factorID);

    factorFields = document.getElementsByClassName(factorID);
    contents = factorFields[0].innerHTML;
    if (contents.length > 0) {
      contents = contents.substring(0, contents.length - 1);
    }
    for (var i = 0; i < factorFields.length; i++) {
        factorFields[i].innerHTML = contents
    }

  }

  // Tracking factoring functionality

  var guessedPairs
  var factorPairs
  var product

  function loadFirstProblem() {
    // console.log('loading first problem')
    setupPage()
    loadNewProblem()
  }

  function loadNewProblem() {
    product = getNumber()
    resetForNewProblem()
    // console.log('loading product: ', product)
    nums = document.getElementsByClassName('numberToFactor');
    // console.log('nums=', nums)
    for (var i = 0; i < nums.length; i++) {
        nums[i].innerHTML = product;
    }
    factorPairs = findFactors(product)
    divs = document.getElementsByClassName('possiblePairs')
    for (var i = 0; i < divs.length; i++) {
        divs[i].innerHTML = factorPairs.length
    }
    setGuessedPairs()
  }

  function resetForNewProblem() {
    factorPairs = []
    guessedPairs = []
    divs = document.getElementsByClassName('factor1')
    for (var i = 0; i < divs.length; i++) {
        divs[i].innerHTML = ""
    }
    divs = document.getElementsByClassName('factor2')
    for (var i = 0; i < divs.length; i++) {
        divs[i].innerHTML = ""
    }
    // document.getElementById('grader').innerHTML = ""
    divs = document.getElementsByClassName('possiblePairs')
    for (var i = 0; i < divs.length; i++) {
        divs[i].innerHTML = ""
    }
    divs = document.getElementsByClassName('guessedPairs')
    for (var i = 0; i < divs.length; i++) {
        divs[i].innerHTML = ""
    }
    setSubmitButtons(true)
  }

  function findFactors(product) {
    // Returns array of L2 arrays of factors for product
    var factorPairs = []
    var i;
    for (i = 0; i < (product / 2) + 1; i++) {
      if ((product % i) == 0) {
        newPair = [i, product / i]
        reversedPair = [product / i, i]
        if (!isInArray(newPair, factorPairs)) {
          factorPairs.push([i, (product / i)])
        }
      }
    }
    return factorPairs
  }

  function isInArray(item, array) {
    // Checks if item (an array of length 2) is in array
    // console.log("in isInArray with:")
    // console.log("item", item, "array", array)
    for (j = 0; j < array.length; j++) {
      if (item[0] == array[j][0] && item[1] == array[j][1] ||
          item[0] == array[j][1] && item[1] == array[j][0]) {
        // console.log(item, "is in", array)
        return true
      }
    }
    return false
  }

  function clicked() {
    submitAnswers()
  }

  function getNumber() {
    // console.log('in getNumber')
    // console.log('mode=', mode)
    var xhr = new XMLHttpRequest();
    var newNumber = 0;
    xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        // console.log("returning ", parseInt(this.response));
        newNumber = parseInt(this.response);
    }};
    xhr.open("POST", "api/get-problem", false);
    xhr.setRequestHeader("content-type", "application/json")
    xhr.send(JSON.stringify({
        "pairs": guessedPairs,
        "mode": mode
    }));
    return newNumber;
  }

  function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
  }

  function submitButtonPress() {
    // console.log("in submitButtonPress");
    displayLeftNumpad()
    if (guessedPairs.length == factorPairs.length) {
      nextProblem()
    } else {
      submitAnswers()
    }
  }

  function setSubmitButtons(submit) {
    allButtons = document.getElementsByClassName('submitButton')
    if (submit) {
      for (var i = 0; i < allButtons.length; i++) {
        allButtons[i].innerHTML = "Submit"
        allButtons[i].className = "btn btn-success numpadbutton submitButton"
      }
    } else {
      for (var i = 0; i < allButtons.length; i++) {
        allButtons[i].innerHTML = "Next Problem"
        allButtons[i].className = "btn btn-warning numpadbutton submitButton"
      }
    }
  }

  function submitAnswers() {
    // console.log("in submitAnswers")
    // product = parseInt(document.getElementById('numberToFactor').innerHTML)
    factor1 = parseInt(document.getElementsByClassName('factor1')[0].innerHTML)
    factor2 = parseInt(document.getElementsByClassName('factor2')[0].innerHTML)

    divs = document.getElementsByClassName('factor1')
    for (var i = 0; i < divs.length; i++) {
        divs[i].innerHTML = ""
    }
    divs = document.getElementsByClassName('factor2')
    for (var i = 0; i < divs.length; i++) {
        divs[i].innerHTML = ""
    }

    // console.log("checking for previous guess")
    if (isInArray([factor1, factor2], guessedPairs)) {
      // document.getElementById('grader').innerHTML = "You already guessed that pair"
      return
    }

    // console.log("checking factors")
    if (checkFactors(product, factor1, factor2)) {
      // Factors 1 and 2 do multiply to Product
      // document.getElementById('grader').innerHTML = "correct!"
      // console.log(typeof factor1)
      if (factor1 < factor2) {
        guessedPairs.push([factor1, factor2])
        // console.log(factor1, "<", factor2)
      } else {
        guessedPairs.push([factor2, factor1])
        // console.log(factor2, "<", factor1)
      }
      setGuessedPairs()
      setPairsRemaining()
    } else {
      // Incorrect factors
      // document.getElementById('grader').innerHTML = "try again!"
    }

    if (guessedPairs.length == factorPairs.length) {
      // setTotalProblemsPassed(parseInt(totalProblemsPassed) + 1)
      setSubmitButtons(false)
    }

  }

  function setTotalProblemsPassed(newAmount) {
    // console.log('setting passed to ', newAmount);
    totalProblemsPassed = newAmount
    divs = document.getElementsByClassName('totalProblemsPassed')
    for (var i = 0; i < divs.length; i++) {
        divs[i].innerHTML = totalProblemsPassed
    }
  }

  function setGuessedPairs() {
    // console.log("in setGuessedPairs")
    var pairsString = ""
    // product = document.getElementById('numberToFactor').innerHTML;
    // Sort guessedPairs by first elements
    // console.log("sorting guessPairs")
    guessedPairs.sort(function(a,b){return a[0] > b[0];});
    // console.log("populating list")
    for (i = 0; i < factorPairs.length; i++) {
      var classes = ""
      // console.log("checking membership")
      if (guessedPairs.length > 0 && isInArray(factorPairs[i], guessedPairs)) {
        // Pair has been guessed
        // console.log("pair has been guessed")
        outString = factorPairs[i][0] + " * " + factorPairs[i][1] + " = " + product
        classes = "guessed"
      } else {
        // Pair has not been guessed
        // console.log("pair has not been guessed")
        outString = "_ * _ = " + product
      }

      pairsString += "<h2 class=\""
      pairsString += classes
      pairsString += "\">"
      pairsString += outString
      pairsString += "</h2>"
    }
    divs = document.getElementsByClassName('guessedPairs')
    for (var i = 0; i < divs.length; i++) {
        divs[i].innerHTML = pairsString
    }
  }

  function setPairsRemaining() {
    // console.log("in setPairsRemaining")
    divs = document.getElementsByClassName('possiblePairs')
    for (var i = 0; i < divs.length; i++) {
        divs[i].innerHTML = (factorPairs.length - guessedPairs.length)
    }
  }

  function checkFactors(product, factor1, factor2) {
    // console.log("in checkFactors")
    if ((product / factor1) == factor2) {
      return true
    } else {
      return false
    }
  }

  function nextProblem() {
    if (guessedPairs.length == factorPairs.length) {
      setTotalProblemsPassed(parseInt(totalProblemsPassed) + 1)
      loadNewProblem()
    }
  }

  function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }

  function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    // console.log(ca)
    for(var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

  // Mode functionality
  // 0 = basic, 1 = advanced

  function setupPage() {
    // console.log("in setupPage");
    // console.log("mode: ", mode);
    setModeButton();
  }

  function toggleMode() {
    // console.log("in toggle mode")
    mode = Math.abs(mode - 1)
    var url = "api/get-total-passed/" + mode
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        totalProblemsPassed = parseInt(this.response);
        setTotalProblemsPassed(totalProblemsPassed);
    }};
    xhr.open("GET", url, true);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhr.send();

    var url2 = "api/set-last-mode/" + mode
    var xhr2 = new XMLHttpRequest();
    xhr2.open("POST", url2, true);
    xhr2.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhr2.send();

    setModeButton();
    loadNewProblem();
  }

  function setModeButton() {
    modeButton = document.getElementById('modeButton')
    if (mode == 0) {
      // Basic mode
      modeButton.className = "btn btn-warning"
      modeButton.innerHTML = "Basic"
    } else {
      // Advanced mode
      modeButton.className = "btn btn-danger"
      modeButton.innerHTML = "Advanced"
    }
  }

  // Development functionality

  function manualGetProduct() {
    // console.log(getNumber())
  }



  function windowSize() {
  // Setting the current height & width
  // to the elements
  if (window.innerWidth < 1000) {
    document.getElementById('landscape_orientation').style.display = 'none';
    document.getElementById('portrait_orientation').style.display = 'block';
    document.getElementById('left_nums').style.display = 'block';
    document.getElementById('right_nums').style.display = 'none';
    displayLeftNumpad();
  } else {
    document.getElementById('portrait_orientation').style.display = 'none';
    document.getElementById('landscape_orientation').style.display = 'block';
    document.getElementById('left_nums').style.display = 'none';
    document.getElementById('right_nums').style.display = 'none';
  }
  // console.log('height', window.innerHeight);
  // console.log('width', window.innerWidth);
}

window.onresize = function() {
    windowSize();
}

window.onload = function() {
    loadFirstProblem();
    windowSize();
}