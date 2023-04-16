import argparse
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright, board: str, page_num: int) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    # Navigate to the current page
    website = 'https://boards.4channel.org/'
    if page_num:
        page.goto(f"{website}{board}/{page_num}")
    else:
        page.goto(f"{website}{board}")
    # Scroll to bottom of the page
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    # Find all thread links and extract thread ids
    thread_links = page.query_selector_all('.thread')
    thread_ids = [link.get_attribute('id') for link in thread_links]
    print(f"{len(thread_ids)} threads found")
    # Loop through each thread id and extract posts
    for thread_id in thread_ids:
         # Construct thread url without the 't'
        thread_url = f'{website}{board}/thread/{thread_id[1:]}'

        # Go to thread page
        page.goto(thread_url)

        # Extract post information using browser console
        output = page.evaluate('''() => {
            let output = "-----\\n";
            let posts = document.querySelectorAll(".postContainer");
            for (let i = 0; i < posts.length; i++) {
                let post = posts[i];
                let number = post.querySelector(".postInfo .postNum").textContent.replace("No.", "");
                let caption = post.querySelector(".postMessage").innerHTML.trim();
                caption = caption.replace(/&gt;/g, ">");
                caption = caption.replace(/<br>/g, "\\n");
                caption = caption.replace(/<[^>]*>/g, "");
                if (caption) {
                    output += "--- " + number + "\\n" + caption + "\\n";
                }
            }
            return output;
        }''')

        # Save output to file
        file_name = f'{thread_id[1:]}.txt'

        # Overwrite existing files with the same name
        with open(file_name, 'w') as f:
            f.write(output)
        print(f'Saved {file_name}')
        

    context.close()
    browser.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape posts from 4chan.')
    parser.add_argument('-b', '--board', type=str, default='a', help='The 4chan board to scrape')
    parser.add_argument('-p', '--page_num', type=int, default=None, help='The starting page number')
    args = parser.parse_args()

    with sync_playwright() as playwright:
        run(playwright, args.board, args.page_num)
