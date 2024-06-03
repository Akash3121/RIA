let r;
let currentDateOne = new Date(new Date().getTime() + 0 * 60 * 60 * 1000);
let currentDateTwo = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
let currentDateThree = new Date(new Date().getTime() + 48 * 60 * 60 * 1000);
let currentDateFour = new Date(new Date().getTime() + 72 * 60 * 60 * 1000);

let one = `${
  currentDateOne.getMonth() + 1
}/${currentDateOne.getDate()}/${currentDateOne.getFullYear()}`;
let two = `${
  currentDateTwo.getMonth() + 1
}/${currentDateTwo.getDate()}/${currentDateTwo.getFullYear()}`;
let three = `${
  currentDateThree.getMonth() + 1
}/${currentDateThree.getDate()}/${currentDateThree.getFullYear()}`;
let four = `${
  currentDateFour.getMonth() + 1
}/${currentDateFour.getDate()}/${currentDateFour.getFullYear()}`;

function first() {
  $("#formDiv").css("display", "none");
  let input = $("input[name=radioName]:checked", "#myForm").val();
  if (input == "place") {
    $("#mainText").css("background-color", "rgb(241, 226, 226)");
    $("#mainText").append(
      `<input type="text" id="place" name="mainText" placeholder="Type a place name"><br><button type="button" id="finalButton">FETCH!</button>`
    );
    $("#finalButton").on("click", () => {
      $("#mainText").css("display", "none");
      let placeName = $("#place").val();
      $.getJSON(
        `https://api.openweathermap.org/data/2.5/forecast?q=${placeName}&units=imperial&appid=a7fe98abecb7645b2f4614acb353cbc0`,
        (data) => {
          r = data;
          final(r);
        }
      );
    });
  }
  if (input == "zipCode") {
    $("#mainText").css("background-color", "rgb(241, 226, 226)");
    $("#mainText").append(
      `<input type="text" id="zipCode" name="mainText" placeholder="Type any ZipCode"><br><input type="text" id="countryCode" name="mainText" placeholder="Type the country code"><br><button type="button" id="finalButton">FETCH!</button>`
    );
    $("#finalButton").on("click", () => {
      $("#mainText").css("display", "none");
      let zip = parseInt($("#zipCode").val());
      let code = $("#countryCode").val();
      $.getJSON(
        `https://api.openweathermap.org/data/2.5/forecast?zip=${zip},${code}&units=imperial&appid=a7fe98abecb7645b2f4614acb353cbc0`,
        (data) => {
          r = data;
          final(r);
        }
      );
    });
  }
  if (input == "co") {
    $("#mainText").css("background-color", "rgb(241, 226, 226)");
    $("#mainText").append(
      `<input type="text" id="lat" name="mainText" placeholder="Type lat"><br><input type="text" id="long" name="mainText" placeholder="Type long"><br><button type="button" id="finalButton">FETCH!</button>`
    );
    $("#finalButton").on("click", () => {
      $("#mainText").css("display", "none");
      let lat = parseFloat($("#lat").val());
      let long = parseFloat($("#long").val());
      $.getJSON(
        `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${long}&units=imperial&appid=a7fe98abecb7645b2f4614acb353cbc0`,
        (data) => {
          r = data;

          final(r);
        }
      );
    });
  }
}

function final(d) {
  let arr = d.list;
  let tempMaxOne = [];
  let tempMaxTwo = [];
  let tempMaxThree = [];
  let tempMaxFour = [];
  let cloudOne = [];
  let cloudTwo = [];
  let cloudThree = [];
  let cloudFour = [];
  let pressureOne = [];
  let pressureTwo = [];
  let pressureThree = [];
  let pressureFour = [];
  let firstDayUnix = arr[0].dt + 86400;
  let secondDayUnix = firstDayUnix + 86400;
  let thirdDayUnix = secondDayUnix + 86400;
  let fourthDayUnix = thirdDayUnix + 86400;
  for (let i = 0; i < arr.length; i++) {
    if (arr[i].dt < firstDayUnix) {
      tempMaxOne.push(arr[i].main.temp_max);
      cloudOne.push(arr[i].clouds.all);
      pressureOne.push(arr[i].main.pressure);
    }
    if (arr[i].dt > firstDayUnix && arr[i].dt < secondDayUnix) {
      tempMaxTwo.push(arr[i].main.temp_max);
      cloudTwo.push(arr[i].clouds.all);
      pressureTwo.push(arr[i].main.pressure);
    }
    if (arr[i].dt > secondDayUnix && arr[i].dt < thirdDayUnix) {
      tempMaxThree.push(arr[i].main.temp_max);
      cloudThree.push(arr[i].clouds.all);
      pressureThree.push(arr[i].main.pressure);
    }
    if (arr[i].dt > thirdDayUnix && arr[i].dt < fourthDayUnix) {
      tempMaxFour.push(arr[i].main.temp_max);
      cloudFour.push(arr[i].clouds.all);
      pressureFour.push(arr[i].main.pressure);
    }
  }

  let tempOneAvg = average(tempMaxOne);
  let tempTwoAvg = average(tempMaxTwo);
  let tempThreeAvg = average(tempMaxThree);
  let tempFourAvg = average(tempMaxFour);
  let cloudOneAvg = average(cloudOne);
  let cloudTwoAvg = average(cloudTwo);
  let cloudThreeAvg = average(cloudThree);
  let cloudFourAvg = average(cloudFour);
  let pressureOneAvg = average(pressureOne);
  let pressureTwoAvg = average(pressureTwo);
  let pressureThreeAvg = average(pressureThree);
  let pressureFourAvg = average(pressureFour);
  $("#mainTableDiv").append(`<table id="mainTable"></table>`);
  $("#mainTable").append(
    ` <thead>
    <tr>
      <th>Date</th>
      <th>Highest Temperature</th>
      <th>Clouds</th>
      <th>Pressure</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td>${one}</td>
        <td>${tempOneAvg}</td>
        <td>${cloudOneAvg}</td>
        <td>${pressureOneAvg}</td>
    </tr>
    <tr>
        <td>${two}</td>
        <td>${tempTwoAvg}</td>
        <td>${cloudTwoAvg}</td>
        <td>${pressureTwoAvg}</td>
    </tr>
    <tr>
        <td>${three}</td>
        <td>${tempThreeAvg}</td>
        <td>${cloudThreeAvg}</td>
        <td>${pressureThreeAvg}</td>
    </tr>
    <tr>
        <td>${four}</td>
        <td>${tempFourAvg}</td>
        <td>${cloudFourAvg}</td>
        <td>${pressureFourAvg}</td>
    </tr>
  </tbody>
  
  
  `
  );
}

function average(arr) {
  let sum = 0;
  for (let i = 0; i < arr.length; i++) {
    sum = sum + arr[i];
  }
  let avg = sum / arr.length;
  avg = avg.toFixed(0);
  return avg;
}
