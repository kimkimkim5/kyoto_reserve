from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import logger
import util
import subprocess


# --- 先ず、以下を実行し、デバッグモードのブラウザを立ちあげる。 ---
command = r'"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir=C:\selenium\chrome-profile'
subprocess.Popen(command, shell=True)
time.sleep(10)

chrome_service = Service(executable_path='c:\chromedriver-win64\chromedriver.exe')

# Chromeオプションを設定
chrome_options = Options()
chrome_options.debugger_address = "localhost:9222"  # デバッグモードのポート番号に合わせる

# 既に開いているChromeブラウザに接続
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# データ登録の操作を実行
# ここにRPAを実施したいURLを登録します。
driver.get('https://g-kyoto.pref.kyoto.lg.jp/reserve_j/core_i/init.asp?SBT=1&Target=_Top&LCD=')

# 現在開かれているタブのハンドルを取得
original_window = driver.current_window_handle

# ===================================================================
# ========================= メイン関数 ===============================
# ===================================================================
def main(): 

    login_flag = 0

    # ==================== 施設予約システム ======================
    logger.debug('施設予約システム START')
    # フレームに切り替え
    driver.switch_to.frame("MainFrame")  # フレーム名 'MainFrame' を使用
    
    # "バスケットボール" のリンクをクリック
    util.link_click(driver, "バスケットボール", 0)
    
    
    # ==================== 所在地選択 ======================
    # "京都市南区" のリンクをクリック
    util.link_click(driver, "京都市南区", 0)
    
    # "検索" をクリック
    xpath = "//input[@class='clsImage']"
    util.xpath_click(driver, xpath, 7)
    

    # ==================== 会館選択 ======================
    # "抽選" をクリック
    xpath = "//input[@alt='予約画面へ']"
    util.xpath_click(driver, xpath, 1)
    
    
    # ==================== 日程選択 ======================
    # "該当月" をクリック
    util.link_click(driver, f"{util.SELECT_MONTH}月", 0)
    
    logger.info(f'★★★★★  {util.SELECT_MONTH}月の登録を実施★★★★★')
    
    for index in util.SELECT_DAY:

        # 念のため、クリアしておく
        xpath = "//input[@name='btn_clear']"
        util.xpath_click(driver, xpath, 0)
        
        # ポップアップ画面
        util.popup_click(driver, util.POPUP_ACCEPT)
        
        # "該当日" のリンクを取得
        logger.info(f'★★★★★       {str(index)}日の登録を実施★★★★★')
        
        # "該当日" のリンクをクリック
        util.link_click(driver, str(index), 0)
        
        # ************ 条件設定 ************
        # "予約可能" のリンクを取得
        #    image000000000：9:30開始   image000001000：13:00開始    image000002000：16:00開始   image000003000：19:00開始
        xpath = "//img[@name='image000001000' and @alt='予約可能']"
        select_element = util.get_elements_xpath(driver, xpath)
        
        if select_element:

            # クリック
            select_element[0].click()
            time.sleep(util.SLEEP_TIME)
        
            logger.info(f'＝＝＝＝＝  {util.SELECT_MONTH}月{str(index)}日の予約をします ＝＝＝＝＝')    
            # ==================== 面施設選択処理画面 ======================
            # 現在のウィンドウハンドルを取得
            original_window = driver.current_window_handle
            # すべてのウィンドウハンドルを取得
            all_windows = driver.window_handles

            # 新しいウィンドウに切り替える
            util.switch_window(driver, all_windows, original_window)

            # ************ 条件設定 ************
            # "予約可能" のリンクを取得
            # 　　　image0：全面  image1：A面  image2：B面
            # xpath = "//img[( @name='image1' or @name='image2' ) and @alt='予約可能 ']"
            xpath = "//img[@name='image0' and @alt='予約可能 ']"
            select_element2 = util.get_elements_xpath(driver, xpath)
            if select_element2:
                
                # クリック
                select_element2[0].click()
                time.sleep(util.SLEEP_TIME)
                
                # "閉じる" のリンクを取得
                xpath = "//input[@name='btn_close']"
                util.xpath_click(driver, xpath, 0)
                
                # ==================== 日程選択 ======================
                # フレームに切り替え
                driver.switch_to.window(original_window)
                driver.switch_to.frame("MainFrame")  # フレーム名 'MainFrame' を使用
                
                # "次へ" のリンクを取得
                xpath = "//input[@alt='次へ']"
                util.xpath_click(driver, xpath, 0)
                
                # ==================== ログイン画面 ======================
                if login_flag == 0:
                    xpath = "//input[@name='txt_usr_cd']"
                    util.set_textbox(driver, xpath, util.KYOTO_FACILITY_USERNAME, 0)
                    
                    # "パスワード" のテキストボックス
                    xpath = "//input[@name='txt_pass']"
                    util.set_textbox(driver, xpath, util.KYOTO_FACILITY_PASSWORD, 0)
                    
                    # "OK" のリンクを取得
                    xpath = "//input[@alt='ＯＫ']"
                    util.xpath_click(driver, xpath, 0)
                    
                    login_flag = 1
                
                # ==================== 紹介画面 ======================
                # "次へ" のリンクを取得
                xpath = "//input[@alt='次へ']"
                util.xpath_click(driver, xpath, 0)

                # ==================== 利用人数画面 ======================
                # "利用人数" のテキストボックス
                xpath = "//input[@name='NUM_1']"
                util.set_textbox(driver, xpath, '10', 0)
                
                # "次へ" のリンクを取得
                xpath = "//input[@alt='次へ']"
                util.xpath_click(driver, xpath, 0)

                # ==================== 予約確認画面 ======================
                # "予約" のリンクを取得
                xpath = "//input[@alt='予約']"
                util.xpath_click(driver, xpath, 0)
            
                # ==================== 内容確認ダイアログ ====================== 
                util.popup_click(driver, util.POPUP_DISMISS)
                logger.info(f'＝＝＝＝＝  {util.SELECT_MONTH}月{str(index)}日の予約は完了しました ＝＝＝＝＝')
                
                # ==================== 画面戻し作業(1) ======================
                # "戻る" のリンクを取得
                xpath = "//input[@name='btn_back']"
                util.xpath_click(driver, xpath, 0)
                
                # ==================== 画面戻し作業(2) ======================
                # "戻る" のリンクを取得
                xpath = "//input[@name='btn_back']"
                util.xpath_click(driver, xpath, 0)

                # ==================== 画面戻し作業(3) ======================
                # "戻る" のリンクを取得
                xpath = "//input[@name='btn_back']"
                util.xpath_click(driver, xpath, 0)
            
            else:
                # "閉じる" のリンクを取得
                xpath = "//input[@name='btn_close']"
                util.xpath_click(driver, xpath, 0)
                logger.info(f'＝＝＝＝＝  A面・B面が空いていない為、{util.SELECT_MONTH}月{str(index)}日の予約はできませんでした ＝＝＝＝＝') 
            
        else:
            logger.info(f'＝＝＝＝＝  19:00が空いていない為、{util.SELECT_MONTH}月{str(index)}日の予約はできませんでした ＝＝＝＝＝')    
    
    
    # ==================== 終了報告 ====================== 
    print("\n★終了★")



if __name__ == '__main__': 
    logger.debug('============== START ==============')
    main()
    logger.debug('============== END ==============')
