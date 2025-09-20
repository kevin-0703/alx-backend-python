##Tasks Breakdown
#0. Parameterize a unit test

Write parameterized tests for utils.access_nested_map.

Check correct outputs for different inputs.

#1. Parameterize a unit test (exceptions)

Test that access_nested_map raises a KeyError for invalid paths.

#2. Mock HTTP calls

Test utils.get_json without making real HTTP requests.

Use unittest.mock.patch to mock requests.get.

#3. Parameterize and patch (memoize)

Test the memoize decorator to ensure caching works correctly.

Verify that a method is only called once even if accessed multiple times.

#4. Parameterize and patch as decorators

Test GithubOrgClient.org method with @patch and @parameterized.expand.

#5. Mocking a property

Test \_public_repos_url by mocking the org property.

#6. More patching

Test public_repos with mocks for \_public_repos_url and get_json.

#7. Parameterize

Test has_license with parameterized inputs and expected outputs.

#8. Integration test: fixtures

Perform integration tests on GithubOrgClient.public_repos.

Use fixtures.py data with @parameterized_class.

Patch requests.get to simulate API responses.
