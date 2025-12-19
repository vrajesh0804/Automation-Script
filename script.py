from playwright.sync_api import sync_playwright

def login_website():
	with sync_playwright() as p:
		browser = p.chromium.launch(headless=False)
		context = browser.new_context()
		page = context.new_page()
		context.clear_cookies()
        # Clear storage (local/session)
		page.goto("https://www.website.com/login")

		page.evaluate("() => { window.localStorage.clear(); window.sessionStorage.clear(); }")

		# Fill username and password fields
		# page.fill("input#username", username)
		# page.fill("input#password", password)

		page.fill("input#username", "username@gmail.com")
		page.fill("input#password", "password")

		# Click on the login button
		page.click("button[type='submit']")

		# Wait for website feed page to load by checking main feed element visibility
		page.wait_for_url("https://www.website.com/feed/*", timeout=20000)
		print("Login successful!")

		# Wait for search input to be visible on top nav
		page.wait_for_selector("#global-nav-search input.search-global-typeahead__input", timeout=10000)

		search_input = page.locator("#global-nav-search input.search-global-typeahead__input")
		search_input.wait_for(state="visible", timeout=10000)
		search_input.fill("software developer")

		# Focus the input to trigger UI
		search_input.click()  

		# Instead of clicking the button, press Enter key inside input
		search_input.press("Enter")


		# Wait for results page to load, looking for results container or HR listing presence
		page.wait_for_selector("div.search-results-container", timeout=15000)
		print("Search results are visible.")

		page.locator("button.artdeco-pill", has_text="People").click()

		# Wait for pagination control to be visible
		while True:
			# Connect button code starts
			# Locate the parent <ul> containing the search result <li> elements
			results_list = page.locator("div.pv0.ph0.mb2.artdeco-card")
			page.wait_for_timeout(5000)
			print(results_list.count())
			for i in range(results_list.count()):
				results = results_list.locator("ul > li.crWvMSTRAKyyMuCYZzfApSMXWHxSmApQYFY")
				count = results.count()
				print("Total count",count)

				for i in range(count):
					li_el = results.nth(i)
					div1 = li_el.locator("div.DiUiCiXquAGYukwIBdOEyFtUQLOKDTOfo")
					div2 = div1.locator("div.lCnclEwBgOLGDyntVMIAMmxqoThxBTUzyGHNqc")
					connect_btn = div2.locator("button.artdeco-button.artdeco-button--2.artdeco-button--secondary")

					# Get username text - usually inside an <a> tag with profile link inside li
					username_el = li_el.locator("a[data-test-app-aware-link] span[dir='ltr']").first
					username = ""
					if username_el.count() > 0:
						username = username_el.inner_text().strip()
						is_visible = connect_btn.is_visible()
						print(f"Username: {username}, Connect visible: {is_visible}")

					if is_visible:
						connect_btn.click()
						page.wait_for_timeout(1000)

						send_without_note_btn = page.locator("button.artdeco-button--primary:has-text('Send without a note')")
						if send_without_note_btn.is_visible():
							send_without_note_btn.click()
							page.wait_for_timeout(1000)

				
				pagination_div = page.locator("div.artdeco-pagination.artdeco-pagination--has-controls")
				if pagination_div.is_visible():
					print("Pagination visible here")

					# Locate the Next button
					next_button = pagination_div.locator("button.artdeco-pagination__button--next")
					print(next_button.is_visible())

					if next_button.get_attribute("disabled") is not None:
						print("No more pages, pagination ended.")
						break

					next_button.click()
					print("Clicked Next, moving to next page...")

		# Connect button code ends

		# Keep browser open for a while to observe after login
		page.wait_for_timeout(15000)
		browser.close()
    

if __name__ == "__main__":
    login_website()
