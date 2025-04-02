// src/config.js

// 模擬 Python 的 sys.platform 來判斷作業系統
const platform = navigator.platform.toLowerCase();
let CHROMEDRIVER_PATH, RANDOM_DATA_JSON_PATH;

if (platform.includes("win")) {
  CHROMEDRIVER_PATH = "C:\\Users\\d1031\\新增資料夾\\unittest\\chormedrive\\chromedriver.exe";
  RANDOM_DATA_JSON_PATH = "C:\\Users\\d1031\\新增資料夾\\unittest\\config\\random_data.json";
} else if (platform.includes("mac")) {
  CHROMEDRIVER_PATH = "/Users/steven/deepseek/seleium/chormedrive/chromedriver";
  RANDOM_DATA_JSON_PATH = "/Users/steven/deepseek/seleium/config/random_data.json";
} else if (platform.includes("linux")) {
  CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver";
  RANDOM_DATA_JSON_PATH = "/app/config/random_data.json";
} else {
  throw new Error("Unsupported OS");
}

const Config = {
  // 全域設定
  ENV: "TestEnv", // 預設環境，可選："TestEnv", "ProdEnv"
  MERCHANT: "Merchant1", // 預設商戶，可選："Merchant1", "Merchant2", "Merchant5", "Merchant7"
  DELAY_SECONDS: 0.5,
  WAIT_TIMEOUT: 10,

  CHROMEDRIVER_PATH,
  RANDOM_DATA_JSON_PATH,

  // 測試環境配置
  TestEnv: {
    MerchantBase: {
      BASE_SC_URL: "http://uat-admin-api.mxsyl.com:5012",
      SC_LOGIN_API: "/api/v1/admin/auth/login",
      AES_KEY_API: "/api/v1/admin/auth/getpasswordencryptkey",
      LOGIN_API: "/v1/member/auth/loginbyname",
      DEPOSIT_API: "/v1/asset/deposit/currency",
      SC_USERNAME: "QA002",
      SC_PASSWORD: "QA002",
      VERIFY_CODE: "123456",
      DP_Amount: "100",
    },
    Merchant1: {
      BASE_URL: "https://uat-newplatform.mxsyl.com",
      LOGIN_URL: "https://uat-newplatform.mxsyl.com/zh-cn/login",
      REGISTER_URL: "https://uat-newplatform.mxsyl.com/zh-cn/register",
      PHONE_NUMBER: "13100000021",
      EMAIL: "hrtqdwmk@sharklasers.com",
      VALID_USERNAME: "cooper005",
      VALID_DP_USERNAME: "cooper024",
      VALID_DP_NAME: "测试",
      VALID_PASSWORD: "1234Qwer",
      VALID_PASSWORD_MD5:
        "J+qUZNvIJnsQ91KG1wDjBxnvIA3w+98epcCr8jN9u03wwEVytx57ScGfoeySN0nex4jiIzG2qfUfRXnSTtsULjPEvtgpTOdEXEH3SKSR1GJEENUxOo7uezgpKrpxobKLJQehXQEeXivDZla7tNe6EDBT6qKsCgmBYMZGNNRaJdmZSG0HkZnZWcJ34/rhQQxEPeU1ZseiK+q3H9Q9RSyB6+fn2wyQtoU4o4BdzjvrapRtLwrIwobiaOH1PeaeIcUKgCX30FQCuYHtOMnKwEBoz4IwuS5z+XFT1XIbdkRMm+FXoZZOQ7BeLCYGgWOEWMhnOQzAKaYkJvI1KYq4OFEraA==",
    },
    Merchant2: {
      BASE_URL: "https://uat2-newplatform.mxsyl.com/",
      LOGIN_URL: "https://uat2-newplatform.mxsyl.com/zh-cn/login",
      REGISTER_URL: "https://uat2-newplatform.mxsyl.com/zh-cn/register",
      PHONE_NUMBER: "",
      EMAIL: "",
      VALID_USERNAME: "",
      VALID_DP_USERNAME: "",
      VALID_PASSWORD: "",
      VALID_PASSWORD_MD5: "",
    },
    Merchant5: {
      BASE_URL: "https://uat5-newplatform.mxsyl",
      LOGIN_URL: "https://uat5-newplatform.mxsyl/zh-cn/login",
      REGISTER_URL: "https://uat5-newplatform.mxsyl/zh-cn/register",
      PHONE_NUMBER: "",
      EMAIL: "",
      VALID_USERNAME: "",
      VALID_DP_USERNAME: "",
      VALID_PASSWORD: "",
      VALID_PASSWORD_MD5: "",
    },
    Merchant7: {
      BASE_URL: "https://uat7-newplatform.mxsyl.com",
      LOGIN_URL: "https://uat7-newplatform.mxsyl.com/zh-cn/login",
      REGISTER_URL: "https://uat7-newplatform.mxsyl.com/zh-cn/register",
      PHONE_NUMBER: "",
      EMAIL: "",
      VALID_USERNAME: "",
      VALID_DP_USERNAME: "",
      VALID_PASSWORD: "",
      VALID_PASSWORD_MD5: "",
    },
  },

  // 正式環境配置
  ProdEnv: {
    MerchantBase: {
      BASE_SC_URL: "https://www.gobackend.xyz/",
      SC_LOGIN_API: "/api/v1/admin/auth/login",
      AES_KEY_API: "/api/v1/admin/auth/getpasswordencryptkey",
      LOGIN_API: "/v1/member/auth/loginbyname",
      DEPOSIT_API: "/v1/asset/deposit/currency",
      SC_USERNAME: "Tech_QA_Tester",
      SC_PASSWORD: "123@Tech_QA_Tester",
      VERIFY_CODE: "123456",
      DP_Amount: "100",
    },
    Merchant1: {
      BASE_URL: "https://www.lt.com/",
      LOGIN_URL: "https://www.lt.com/zh-cn/login",
      REGISTER_URL: "https://www.lt.com/zh-cn/register",
      PHONE_NUMBER: "",
      EMAIL: "",
      VALID_USERNAME: "",
      VALID_DP_USERNAME: "",
      VALID_PASSWORD: "",
      VALID_PASSWORD_MD5: "",
    },
    Merchant2: {
      BASE_URL: "https://www.mrcatgo.com",
      LOGIN_URL: "https://www.mrcatgo.com/zh-cn/login",
      REGISTER_URL: "https://www.mrcatgo.com/zh-cn/register",
      PHONE_NUMBER: "",
      EMAIL: "",
      VALID_USERNAME: "",
      VALID_DP_USERNAME: "",
      VALID_PASSWORD: "",
      VALID_PASSWORD_MD5: "",
    },
    Merchant5: {
      BASE_URL: "https://www.letou1.vip",
      LOGIN_URL: "https://www.letou1.vip/zh-cn#login",
      REGISTER_URL: "https://www.letou1.vip/zh-cn#register",
      PHONE_NUMBER: "",
      EMAIL: "",
      VALID_USERNAME: "",
      VALID_DP_USERNAME: "",
      VALID_PASSWORD: "",
      VALID_PASSWORD_MD5: "",
    },
    Merchant7: {
      BASE_URL: "https://vwin158.com",
      LOGIN_URL: "https://vwin158.com/zh-cn/login",
      REGISTER_URL: "https://vwin158.com/zh-cn/register",
      PHONE_NUMBER: "",
      EMAIL: "",
      VALID_USERNAME: "",
      VALID_DP_USERNAME: "",
      VALID_PASSWORD: "",
      VALID_PASSWORD_MD5: "",
    },
  },

  // 動態取得當前配置
  getCurrentConfig(env) {
    const envClass = this[env || this.ENV];
    const merchantConfig = envClass[this.MERCHANT];
    return merchantConfig;
  },

  // 模擬 Python 的隨機資料生成方法
  generateRandomUsername() {
    const timestamp = new Date().toISOString().replace(/[-:T.]/g, "").slice(0, 14);
    const randomUsername = `QAM1${timestamp}`;
    // 由於前端無法直接寫入檔案，這裡僅返回 username
    return randomUsername;
  },

  generateJapanesePhoneNumber() {
    const prefixes = ["070", "080", "090"];
    const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
    const remainingDigits = Array(8)
      .fill()
      .map(() => Math.floor(Math.random() * 9) + 1)
      .join("");
    const japanesePhone = prefix + remainingDigits;
    return japanesePhone;
  },

  generateRandomEmail() {
    const username = this.generateRandomUsername();
    const email = `${username}@gmail.com`;
    return email;
  },
};

export default Config;