from playwright.sync_api import sync_playwright,Page,Request,Response
import xml.etree.ElementTree as ET
import time,re,math,base64,html
with open('credentials') as f:
    _=f.read().split('\n')
    USERNAME=_[0]
    PASSWORD=_[1]
    del _


def main():
    def find_in_activity_data(xml_string, element_name):
            root = ET.fromstring(xml_string)
            element = root.find('.//ActivityData/'+str(element_name))
            if element is not None:
                return element.text
    def exists_in_activity_data(xml_string,element_name):
        root = ET.fromstring(xml_string)
        element = root.find('.//ActivityData/'+str(element_name))
        return element is not None
    # Mathletic's decoding and their goofy naming
    def decode_mathletics_answer(encoded_base64):
        sdfs = "nihonium"

        def biffle(e):
            return fred(baffle(e).replace(sdfs, ""))

        def baffle(e, t=13):
            if not isinstance(e, str):
                return ""
            t = rotate_by(t)
            return ''.join([convert_to_char(t(convert_to_char_code(char))) for char in e])

        def convert_to_char_code(e):
            return ord(e)

        def convert_to_char(e):
            return chr(e)

        def rotate_by(t):
            def rotate(e):
                if 65 <= e <= 90:
                    return e + t if e + t <= 90 else e + t - 90 + 64
                elif 97 <= e <= 122:
                    return e + t if e + t <= 122 else e + t - 122 + 96
                else:
                    return e
            return rotate

        def fred(e):
            n = base64.b64decode(e)
            try:
                return n.decode('utf-8')
            except UnicodeDecodeError:
                return n.decode('latin1')

        

        return biffle(encoded_base64)
    def filter_urls(request:Response):
        match=re.search(r'activitycontentscreen.mathletics.com/question/(\d+)/(.*?)/(.*)',request.url)
        if match:
            response=decode_mathletics_answer(request.text())
            if response:
                questions=[]
                def decode_html(h):
                    return html.unescape(h)
                for x in range(20): # I dont think anything is more than 20 "questions"
                    e=find_in_activity_data(response,'actQuestionText'+str(x))
                    if e:questions.append(decode_html(e))
                answer=find_in_activity_data(response,'actAnswerEnglish0')
                qtype=None
                if exists_in_activity_data(response,'actQuestionSelect'):
                    qtype='select'
                print('Found type:',qtype)
                print('Found "Questions"')
                for q in questions:
                    print(q)
                print('Found Answer:',answer)
                print('\n'*32)
                print('\nInstructions:')
                if qtype=='select':
                    print(f'  Select option #{answer}')
                else:
                    print(f'  Unknown Type. Answer: {answer}')

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context('Browser/browser_data',headless=False)
        browser.on('response',filter_urls)
        page:Page = browser.new_page()
        page.goto("https://sign-in.mathletics.com/")
        page.wait_for_selector('button[type="submit"]')
        # Sign in
        page.fill('#userName', USERNAME)
        page.fill('#password', PASSWORD)
        page.click('button[type="submit"]')

        page.wait_for_timeout(9999999)
        # input('Press Enter to close the browser...')

main()
