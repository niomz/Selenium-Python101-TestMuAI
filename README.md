# Selenium Python 101 — TestMu AI Assignment

Automates all three scenarios in the supplied assignment PDF:
1. Simple Form Demo — enter a message and verify the displayed result.
2. Drag & Drop Sliders — move the default-15 slider to 95.
3. Input Form Submit — check empty-form validation, fill the form, select
   United States by visible text, submit, and verify the success message.

## Browser / OS matrix
- Chrome 128.0 / Windows 10
- Microsoft Edge 127.0 / macOS Ventura
- Firefox 130.0 / Windows 11
- Internet Explorer 11.0 / Windows 10

Confirm exact availability and capability spelling in the TestMu AI
Capabilities Generator. IE 11 is legacy and may not be available on every grid.

## Windows setup
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` with your TestMu AI username and access key. Never commit `.env`.

The default remote endpoint is `https://hub.lambdatest.com/wd/hub`.
Verify the endpoint and generated capabilities in your TestMu AI account.

## Run all 12 scenario/environment combinations in parallel
```powershell
pytest -n 4 -v -s
```
Run only scenario 1:
```powershell
pytest -n 4 -v -s -k scenario_1
```

The 20-second pytest timeout is set in `pytest.ini`. Each remote session
enables `video`, `visual` (screenshots), `network`, and `console` logs.
Session IDs are printed in the terminal and also appear in the TestMu AI
Automation Dashboard.

Selectors are based on the Selenium Playground demo structure. If the live
site changes, inspect its DOM and update the selectors. Browser-native
validation wording varies, so the test checks that an invalid required field
and a non-empty validation message are present.
