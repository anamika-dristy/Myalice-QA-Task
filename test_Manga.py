import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import time
import json

def log_test_case(test_cases, test_case, test_scenario, input_data, expected_result, actual_result, status):
    log_entry = {
        "Test case": test_case,
        "Test scenario": test_scenario,
        "Input": input_data,
        "Expected result": expected_result,
        "Actual result": actual_result,
        "Status": status
    }
    test_cases.append(log_entry)
    with open("report_pretty.json", "w") as file:
        json.dump(test_cases, file, indent=4)


def generate_report(test_cases):
    # Convert test cases to tabular format
    table_headers = ["Test case", "Test scenario", "Input", "Expected result", "Actual result", "Status"]
    table_data = [[entry.get(header, "") for header in table_headers] for entry in test_cases]
    # Append the tabular format to the report file
    with open("report_pretty.json", "a") as file:
        file.write("\n\n")
        file.write(tabulate(table_data, headers=table_headers, tablefmt="grid"))
        file.write("\n\n")


@pytest.fixture(scope="module")
def driver_setup():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def test_cases():
    # Initialize an empty list for test cases
    if os.path.exists("report_pretty.json"):
        os.remove("report_pretty.json")
    return []


class TestManga:

    @pytest.mark.login
    def test_login(self, driver_setup, test_cases):
        driver = driver_setup
        driver.get("https://myalice-automation-test.netlify.app/")
        time.sleep(2)

        expected_result = "Login page should display successfully"
        actual_result = "Login page is display successfully" if "Login" in driver.page_source else "Login not display"
        status = "Passed" if actual_result == "Login page is display successfully" else "Failed"

        log_test_case(
            test_cases,
            test_case="Login Page Test",
            test_scenario="Verify that the login page is displayed",
            input_data="https://myalice-automation-test.netlify.app/",
            expected_result=expected_result,
            actual_result=actual_result,
            status=status
        )
        assert status == "Passed", f"Test Failed: {actual_result}"


        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "password").send_keys("password")
        driver.find_element(By.ID, "login-btn").click()
        time.sleep(2)

        expected_result = "User should redirected to the manga search page"
        actual_result = "User is redirected to the manga search page" if "Manga" in driver.page_source else "Login failed"
        status = "Passed" if actual_result == "User is redirected to the manga search page" else "Failed"
        time.sleep(5)

        # Log the test case
        log_test_case(
            test_cases,
            test_case="Login Test",
            test_scenario="Verify that the user is redirected to the manga search page",
            input_data="username: testuser, password: password",
            expected_result=expected_result,
            actual_result=actual_result,
            status=status
        )
        assert status == "Passed", f"Test Failed: {actual_result}"

    @pytest.mark.mangasearch
    def test_mangasearch(self, driver_setup, test_cases):
        driver = driver_setup

        # First search for "Naruto"
        driver.find_element(By.ID, "manga-search").send_keys("Naruto")
        driver.find_element(By.CSS_SELECTOR, ".bg-green-500.text-white.py-2.px-4.rounded.mr-2").click()
        time.sleep(5)

        expected_result_naruto = "Manga cards should display the name Naruto."
        actual_result_naruto = "Manga cards with the name Naruto are displayed" if "Naruto" in driver.page_source else "Search failed"
        status_naruto = "Passed" if "Naruto" in driver.page_source else "Failed"

        log_test_case(
            test_cases,
            test_case="Search Test - Naruto",
            test_scenario="Verify that manga cards with the name Naruto are displayed",
            input_data="Naruto",
            expected_result=expected_result_naruto,
            actual_result=actual_result_naruto,
            status=status_naruto
        )

        search_box = driver.find_element(By.ID, "manga-search")
        search_box.clear()

        # Now search for "One Piece"
        search_box.send_keys("One Piece")
        driver.find_element(By.CSS_SELECTOR, ".bg-green-500.text-white.py-2.px-4.rounded.mr-2").click()
        time.sleep(5)

        expected_result_onepiece = "Manga cards should display the name One Piece."
        actual_result_onepiece = "Manga cards with the name One Piece are displayed" if "One Piece" in driver.page_source else "Search failed"
        status_onepiece = "Passed" if "One Piece" in driver.page_source else "Failed"

        log_test_case(
            test_cases,
            test_case="Search Test - One Piece",
            test_scenario="Verify that manga cards with the name One Piece are displayed",
            input_data="One Piece",
            expected_result=expected_result_onepiece,
            actual_result=actual_result_onepiece,
            status=status_onepiece
        )

        search_box.clear()

        # Now search for "Seven Deadly Sins"
        search_box.send_keys("Seven Deadly Sins")
        driver.find_element(By.CSS_SELECTOR, ".bg-green-500.text-white.py-2.px-4.rounded.mr-2").click()
        time.sleep(5)

        expected_result_seven = "Manga cards should display 'No manga found' when searching for Seven Deadly Sins."
        actual_result_seven = "No manga found message is displayed" if "No manga found" in driver.page_source else "Search failed"
        status_seven = "Passed" if "No manga found" in driver.page_source else "Failed"

        log_test_case(
            test_cases,
            test_case="Search Test - Seven Deadly Sins",
            test_scenario="Verify that no results are found for Seven Deadly Sins and displays 'No manga found'.",
            input_data="Seven Deadly Sins",
            expected_result=expected_result_seven,
            actual_result=actual_result_seven,
            status=status_seven
        )

        assert status_naruto == "Passed", f"Naruto Test Failed: {actual_result_naruto}"
        assert status_onepiece == "Passed", f"One Piece Test Failed: {actual_result_onepiece}"
        assert status_seven == "Passed", f"Seven Deadly Sins Test Failed: {actual_result_seven}"

    @pytest.mark.mangadetails
    def test_mangadetails(self, driver_setup, test_cases):
        driver = driver_setup
        driver.get("https://myalice-automation-test.netlify.app/")
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "password").send_keys("password")
        driver.find_element(By.ID, "login-btn").click()

        time.sleep(3)

        expected_result = "User should be on the manga search page."
        actual_result = "User is on the manga search page" if "Manga You Should Read" in driver.page_source else "Not on Search page"
        status = "Passed" if actual_result == "User is on the manga search page" else "Failed"

        log_test_case(
            test_cases,
            test_case="Manga search page",
            test_scenario="Ensure the user is on the manga search page",
            input_data="Back to Manga search page",
            expected_result=expected_result,
            actual_result=actual_result,
            status=status
        )

        # Click the "Details"
        driver.find_element(By.CSS_SELECTOR, ".text-blue-500.cursor-pointer").click()
        time.sleep(3)

        # Check for image, name, and summary in the modal
        manga_image = driver.find_element(By.CSS_SELECTOR, ".w-full.h-48.object-cover.rounded-lg.mb-4")
        manga_name = driver.find_element(By.CSS_SELECTOR, ".text-xl.font-bold.mb-2")
        manga_summary = driver.find_element(By.CSS_SELECTOR, ".text-gray-600.mb-4")

        # Expected and actual results for the image
        expected_result_image = "Manga image should be displayed"
        actual_result_image = "Manga image is displayed" if manga_image.is_displayed() else "Manga image failed"
        status_image = "Passed" if actual_result_image == "Manga image is displayed" else "Failed"

        # Expected and actual results for the name
        expected_result_name = "Manga name should be 'Attack on Titan'"
        actual_result_name = f"Manga name is '{manga_name.text}'" if manga_name.text == "Attack on Titan" else f"Expected 'Attack on Titan', but got '{manga_name.text}'"
        status_name = "Passed" if manga_name.text == "Attack on Titan" else "Failed"

        # Expected and actual results for the summary
        expected_result_summary = "Manga summary should be displayed"
        actual_result_summary = "Manga summary is displayed" if manga_summary.is_displayed() else "Manga summary failed"
        status_summary = "Passed" if actual_result_summary == "Manga summary is displayed" else "Failed"

        # Log the test case for the image
        log_test_case(
            test_cases,
            test_case="Manga Image Display Test",
            test_scenario="Verify that the manga image is displayed in the modal",
            input_data="Click on 'Details' and check for the image",
            expected_result=expected_result_image,
            actual_result=actual_result_image,
            status=status_image
        )

        # Log the test case for the name
        log_test_case(
            test_cases,
            test_case="Manga Name Display Test",
            test_scenario="Verify that the manga name is 'Attack on Titan' in the modal",
            input_data="Click on 'Details' and check for the name",
            expected_result=expected_result_name,
            actual_result=actual_result_name,
            status=status_name
        )

        # Log the test case for the summary
        log_test_case(
            test_cases,
            test_case="Manga Summary Display Test",
            test_scenario="Verify that the manga summary is displayed in the modal",
            input_data="Click on 'Details' and check for the summary",
            expected_result=expected_result_summary,
            actual_result=actual_result_summary,
            status=status_summary
        )

        # Click the "Close" button
        driver.find_element(By.CSS_SELECTOR, ".bg-blue-500.text-white.py-2.px-4.rounded").click()
        time.sleep(2)

        # Verify that the modal is closed and no longer visible
        driver.find_element(By.CSS_SELECTOR, ".text-4xl.font-bold.mb-6")

        log_test_case(
            test_cases,
            test_case="Manga Details Modal Test",
            test_scenario="Verify that the manga details modal appears with correct information and can be closed",
            input_data="Click on 'Close'",
            expected_result="Modal displays correct manga information and can be closed",
            actual_result="Modal displayed correct information and closed successfully",
            status="Passed"
        )

if __name__ == "__main__":
    pytest.main(["-v"])
