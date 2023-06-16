const steeringWheel = document.querySelector(".steeringWheel");
const steeringAngleIndicator = document.querySelector("#steeringAngleIndicator");

function getHandleAngle() {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/datatrans", true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      data = xhr.responseText;
      // var data = JSON.parse('"' + xhr.responseText + '"'); // JSON 형식의 응답 데이터 파싱
      // data =
      arr = [];
      arr = data.split(",");
      arr = Array(arr);
      console.log(arr);
    }
  };
  xhr.send();
}

// 1초마다 핸들 각도 가져오기
setInterval(getHandleAngle, 500);
