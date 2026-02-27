# Israeli Utility Portal Reference

Browser automation guide for collecting monthly bills from Israeli utility providers.

## Israel Electric Corporation (IEC / חברת החשמל)

- **Portal:** https://www.iec.co.il
- **Customer area:** Login via personal area (אזור אישי)
- **Login method:** ID number (teudat zehut) + password, or mobile phone OTP
- **Bill location:** My Bills (החשבוניות שלי) section
- **Download format:** PDF
- **2FA:** May require SMS OTP on first login or new device
- **Automation notes:** Login page uses standard form submission. After login, navigate to the bills section and select the relevant billing period. PDF download link is available per bill.

## Bezeq (בזק)

- **Portal:** https://www.bezeq.co.il
- **Customer area:** Personal area (אזור אישי)
- **Login method:** Phone number + password, or ID + last 4 digits of phone
- **Bill location:** Invoices section (חשבוניות)
- **Download format:** PDF
- **2FA:** SMS OTP may be required
- **Automation notes:** The portal may require cookie consent dismissal before login. Bill history is accessible from the account dashboard.

## Partner Communications (פרטנר)

- **Portal:** https://www.partner.co.il
- **Customer area:** My Partner (פרטנר שלי)
- **Login method:** Phone number + password or OTP
- **Bill location:** Billing section (חיובים / חשבוניות)
- **Download format:** PDF
- **2FA:** OTP via SMS to the registered phone number
- **Automation notes:** Partner's portal is a single-page application (SPA). Wait for dynamic content to load before attempting to locate bill elements. Bill PDFs may open in a new tab.

## HOT Telecom (HOT)

- **Portal:** https://www.hot.net.il
- **Customer area:** HOT personal area
- **Login method:** ID number + password or phone-based OTP
- **Bill location:** Invoices section in account management
- **Download format:** PDF
- **2FA:** SMS or email OTP
- **Automation notes:** HOT portal may combine TV, internet, and phone bills into a single invoice. Ensure the correct service is selected when downloading.

## Municipal Water Corporations (תאגידי מים)

Water billing varies by municipality. Common providers:

| City/Region | Provider | Portal |
|-------------|----------|--------|
| Tel Aviv | Mei Avivim (מי אביבים) | meiavivim.co.il |
| Jerusalem | Hagihon (גיחון) | hagihon.co.il |
| Haifa | Mei Carmel (מי כרמל) | meicarmel.co.il |
| Be'er Sheva | Mei Sheva (מי שבע) | meisheva.co.il |

- **Login method:** Varies — typically account number + ID or phone-based OTP
- **Bill location:** Account/billing section
- **Download format:** PDF (most providers)
- **Automation notes:** Each water corporation has a different portal structure. When setting up automation for a new city, inspect the login flow and bill download path manually first.

## Arnona (Municipal Property Tax / ארנונה)

- **Portal:** Municipality-specific (each city runs its own portal)
- **Common portals:**
  - Tel Aviv: https://www.tel-aviv.gov.il (linked to municipal services)
  - Jerusalem: https://www.jerusalem.muni.il
  - Haifa: https://www.haifa.muni.il
- **Login method:** ID number + property account number, or via gov.il identity
- **Bill location:** Arnona payments section
- **Download format:** PDF or printable page
- **2FA:** May require gov.il (Rishui Meukhad) authentication
- **Automation notes:** Arnona portals are typically simpler but vary significantly between municipalities. Some may not offer direct PDF download — in that case, use browser print-to-PDF.

## General Automation Tips

1. **Session management:** Store session cookies to avoid repeated logins within the same collection run.
2. **Rate limiting:** Add short delays (2-3 seconds) between page navigations to avoid triggering anti-bot protections.
3. **Error handling:** If a portal returns a CAPTCHA or blocks access, alert the user and skip to the next provider.
4. **Credential storage:** Never hardcode credentials. Use environment variables or a secure credential store.
5. **Headless mode:** Some portals may detect headless browsers. If login fails, try with a visible browser window.
6. **PDF validation:** After downloading, verify the PDF is not corrupted (file size > 0, valid PDF header).
