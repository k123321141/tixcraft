// content.js

console.log("Content script loaded - Monitoring for captcha image...");

// 檢查圖片是否存在並處理
function solveCaptcha() {
  console.log("Starting captcha solver...");

  const captchaImg = document.getElementById("TicketForm_verifyCode-image");
  const captchaInput = document.getElementById("TicketForm_verifyCode");

  if (captchaImg && captchaInput) {
    console.log("Captcha image and input field found.");

    // 創建 canvas 以獲取圖片的 base64
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    // 設定 canvas 的大小與圖片相同
    const img = new Image();
    img.crossOrigin = "Anonymous";
    img.src = captchaImg.src;

    img.onload = () => {
      console.log("Captcha image loaded.");

      canvas.width = img.width;
      canvas.height = img.height;
      context.drawImage(img, 0, 0);

      // 將圖片轉為 base64
      const base64Image = canvas.toDataURL("image/png").split(",")[1];
      console.log("Captcha image converted to base64.");

      // 發送 POST 請求到 localhost:9487/solve_captcha
      fetch("http://localhost:9487/solve_captcha", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ img_b64str: base64Image })
      })
        .then(response => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then(captchaJson => {
          console.log("Captcha solved. Response received:", captchaJson["result"]);

          // 將回傳的文字填入驗證碼輸入框
          captchaInput.value = captchaJson["result"];
          console.log("Captcha input field updated.");
        })
        .catch(error => console.error("Error while solving captcha:", error));
    };

    img.onerror = () => {
      console.error("Failed to load captcha image.");
    };

    // 停止觀察，避免重複觸發
    observer.disconnect();
  } else {
    console.log("Captcha image or input field not found on this page.");
  }
}

// 使用 MutationObserver 來監視 DOM 的變化
const observer = new MutationObserver((mutationsList, observer) => {
  for (const mutation of mutationsList) {
    if (mutation.type === "childList") {
      // 當圖片元素出現時執行 solveCaptcha
      if (document.getElementById("TicketForm_verifyCode-image")) {
        console.log("Captcha image detected in DOM.");
        solveCaptcha();
      }
    }
  }
});

// 開始觀察整個 document 的變動
observer.observe(document, { childList: true, subtree: true });

