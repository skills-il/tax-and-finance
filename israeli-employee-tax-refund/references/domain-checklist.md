# Domain Coverage Checklist: israeli-employee-tax-refund

Generated: 2026-05-12 via research on: mas.gov.il, kolzchut.org.il, btl.gov.il, pensuni.com, supermarker.themarker.com, moreinvest.co.il, gov.il official notices

## Must cover (core)

- [ ] קריאת טופס 106 (אישור שנתי על משכורת ומס שנוכה). Identify the four refund-driver fields: שדה 042 (סה"כ מס שנוכה במקור), שדה 158/172 (משכורת חייבת), שדה 218/219 (הפקדה לקרן השתלמות), חודשי עבודה (לזיהוי שנה חלקית). source: https://www.kolzchut.org.il/he/%D7%98%D7%95%D7%A4%D7%A1_106. why core: every refund claim starts from Form 106; without correctly reading these fields the skill cannot compute the gap between withheld tax and actual liability.

- [ ] טופס 135. דו"ח מקוצר לשכיר המבקש החזר מס. When to use it (employees who voluntarily request a refund and are not obligated to file 1301), how to file (manually via משרד שומה or via the Public Inquiry System), required attachments. source: https://www.gov.il/he/service/itc135. why core: Form 135 is the canonical voluntary-refund form for salaried employees per Tax Authority procedure; it is what the skill ultimately fills.

- [ ] מערכת מקוונת להחזר מס לשכירים (secapp.taxes.gov.il / portal.taxes.gov.il). When the online track applies vs the manual Form 135 (the online portal is available to those not obligated to file an annual return; obligated filers must use Form 1301 alongside refund computation), what it auto-populates (Form 106 data from employer withholding feeds), what the user uploads (PDF scans of supporting documents). source: https://www.gov.il/he/pages/sa300821-2. why core: the online portal is the preferred channel since tax year 2019 and significantly reduces friction vs. paper Form 135.

- [ ] חלון התיישנות. 6 שנים אחורה מתום שנת המס לפי סעיף 160 לפקודת מס הכנסה. Confirmed in force as of 2026: refund claims for tax year 2020 can be filed until 31.12.2026; for 2021 until 31.12.2027. source: https://www.kolzchut.org.il/he/%D7%94%D7%97%D7%96%D7%A8_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94. why core: defines the universe of tax years the skill can scan and the user's deadline.

- [ ] נקודות זיכוי 2026. ערך נקודה חודשי 242 ₪ / שנתי 2,904 ₪, זכאות בסיסית 2.25 לתושב, 2.75 לאישה, נקודות לילדים לפי גיל, להורה יחיד, לעולה חדש (סעיף 35), למסיים תואר ראשון (1 נק' עד 3 שנות מס לסיימי 2023+, נק' אחת בשנה לבוגרי 2014-2022), חצי נק' לתואר שני (סעיף 40ג), נקודות זיכוי ללוחמי מילואים לפי תיקון 283 (סעיף 39ב). source: https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94. why core: undeclared/under-applied credit points are the most common refund trigger for salaried employees; without correct 2026 values the refund estimate is wrong.

- [ ] מדרגות מס 2026 לשכירים. 10% עד 7,010 ₪/חודש, 14% עד 10,060 ₪/חודש, 20% עד 19,000 ₪/חודש, 31% עד 25,100 ₪/חודש, 35% עד 46,690 ₪/חודש, ומעל זה 47% (בתוספת מס יסף 3% מעל תקרה שנתית של 721,560 ₪). source: https://www.kolzchut.org.il/he/%D7%9E%D7%93%D7%A8%D7%92%D7%95%D7%AA_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94. why core: refund amount = tax actually due under brackets minus tax actually withheld.

- [ ] החלפת מקום עבודה / שני מעבידים באותה שנה. When each employer ran the tax-withholding calculation as if its salary was the worker's only income; without a תיאום מס mid-year the cumulative withholding over-shoots. source: https://www.kolzchut.org.il/he/%D7%94%D7%97%D7%96%D7%A8_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94. why core: classic single-largest refund driver for mid-career employees.

- [ ] תקופות אבטלה / חל"ת / חופשת לידה במהלך שנת המס. When monthly withholding assumed a full 12-month salary but actual months worked were fewer; cross-reference with Bituach Leumi gimul. source: https://www.kolzchut.org.il/he/%D7%97%D7%95%D7%A4%D7%A9%D7%94_%D7%9C%D7%9C%D7%90_%D7%AA%D7%A9%D7%9C%D7%95%D7%9D. why core: extremely common trigger after pregnancy/parenthood leave or layoffs.

- [ ] שירות מילואים. נקודות זיכוי לפי סעיף 39ב לפקודה (תיקון 283 התשפ"ו-2025): 30-39 ימי מילואים = 0.5 נק' (1,452 ₪); 40-49 ימים = 0.75 נק' (2,178 ₪); 50+ ימים = 1 נק' מלאה (2,904 ₪); כל 5 ימים נוספים = 0.25 נק' עד תקרה של 4 נק' (11,616 ₪); מימוש בהחזר מס בשנת המס שאחרי השירות. source: https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%9C%D7%95%D7%97%D7%9E%D7%99_%D7%9E%D7%99%D7%9C%D7%95%D7%90%D7%99%D7%9D. why core: massive refund driver post-7.10; rarely auto-applied by employers.

- [ ] תרומות למוסד ציבורי מאושר לפי סעיף 46 לפקודה. מינימום שנתי 207 ₪, תקרה 10,354,816 ₪ או 30% מההכנסה החייבת (הנמוך), שיעור זיכוי 35% מסכום התרומה. החל מ-1.1.2026 רק תרומות שדווחו למערכת הדיגיטלית של רשות המסים יזכו בהטבה. source: https://www.kolzchut.org.il/he/%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%91%D7%A9%D7%9C_%D7%AA%D7%A8%D7%95%D7%9E%D7%94_(%D7%A1%D7%A2%D7%99%D7%A3_46). why core: most common voluntary deduction not auto-applied in payroll.

- [ ] זיכוי תושב יישוב מזכה. לפי סעיף 11 לפקודת מס הכנסה ולחוק הנגב/הגליל. דורש מגורי קבע (מרכז חיים) ביישוב לפחות 12 חודשים רצופים. רשימת היישובים והשיעורים מתפרסמת שנתית בהודעת מס הכנסה. source: https://www.kolzchut.org.il/he/%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%AA%D7%95%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A4%D7%A8%D7%99%D7%A4%D7%A8%D7%99%D7%94. why core: residents of dozens of localities routinely miss this.

- [ ] זמן טיפול וריבית על החזר באיחור. לשכיר: בתוך שנה מיום השומה או שנתיים מתום שנת המס (הגבוה מביניהם); ההחזר משולם בתוספת הפרשי הצמדה וריבית של 4% שנתי. source: https://www.kolzchut.org.il/he/%D7%94%D7%97%D7%96%D7%A8_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94. why core: users need realistic timeline expectations.

- [ ] נקודות זיכוי לחייל משוחרר / בוגר שירות לאומי-אזרחי. 2 נק' (שירות מלא: 23+ חודשים גברים, 22+ נשים) או נק' אחת (שירות קצר מעל שנה), למשך 36 חודשים מהחודש שאחרי השחרור; שווי 2026: 2 נק' = 5,808 ₪, נק' אחת = 2,904 ₪. source: https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%97%D7%99%D7%99%D7%9C%D7%99%D7%9D_%D7%9E%D7%A9%D7%95%D7%97%D7%A8%D7%A8%D7%99%D7%9D_%D7%95%D7%9E%D7%A1%D7%99%D7%99%D7%9E%D7%99_%D7%A9%D7%99%D7%A8%D7%95%D7%AA_%D7%9C%D7%90%D7%95%D7%9E%D7%99-%D7%90%D7%96%D7%A8%D7%97%D7%99. why core: highest-incidence miss for the young-employee / reservist persona; the חייל משוחרר box on Form 101 is routinely left un-ticked.

- [ ] נקודות זיכוי בגין ילד או בן/בת זוג נטול יכולת לפי סעיף 45(א). 2 נק' (5,808 ₪/שנה) לכל ילד משותק / עיוור / עם מוגבלות שכלית-התפתחותית, כולל ילד בן/בת הזוג; טופס 116א; אינו מיושם במקור. source: https://www.gov.il/he/service/itc-request-for-tax-credits-disabled-relative. why core: distinct from the taxpayer's own Section 9(5) exemption; hits the special-needs-parent population.

- [ ] זיכוי בשל החזקת קרוב במוסד לפי סעיף 44. 35% מההפרש בין ששולם לבין 12.5% מהכנסת המבקש; הכנסת הקרוב עד 188,000 ₪ (יחיד) / 301,000 ₪ (זוג) ב-2026; טופס 116; מוציא זה את זה עם סעיף 45(א). source: https://www.kolzchut.org.il/en/Income_Tax_Credit_for_a_Parent_or_Spouse_Living_in_an_Institution. why core: named standalone credit for the sandwich-generation filer; never applied at source.

## Should cover (advanced / edge cases)

- [ ] פטור ממס הכנסה לנכה לפי סעיף 9(5) לפקודה. לעיוור, לנכה רפואי 100%, או לנכה 90%+ עקב פגיעה באיברים שונים; תקרת הכנסה מיגיעה אישית פטורה ממס נקבעת שנתית ומשתנה לפי משך הנכות (מעל/מתחת 365 יום) ולפי קצבה חודשית. source: https://www.kolzchut.org.il/he/%D7%94%D7%97%D7%96%D7%A8_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94. why advanced: requires medical-board determination; skill should detect signal and route to qualified consultant rather than auto-fill.

- [ ] זיכוי הפקדה לפנסיה וביטוח חיים לפי סעיפים 45א ו-47 לפקודה. סעיף 45א מקנה זיכוי של 35% מסכום ההפקדה על שכר מבוטח. סעיף 47 מאפשר ניכוי על הפקדה עצמאית לקופת גמל לקצבה על שכר לא מבוטח, עם תקרת הכנסה מזכה של 9,700 ש"ח לחודש בשנת 2026 (סעיף 47(א)(1)(1), לוח הניכויים של רשות המסים). שיעור הניכוי על הכנסת עבודה שאינה מבוטחת הוא 5% לפי סעיף 47(ב)(2)(א), כלומר עד 485 ש"ח לחודש. בסעיף 47 שיעור ה-7% חל על הכנסה מזכה שאיננה הכנסת עבודה, ולא על שכר. אין לבלבל זאת עם הזיכוי לפי סעיף 45א(ד)(2)(ב)(2), שם דווקא 7% מההכנסה המזכה חלים על שכיר, ובתקרת הכנסה מזכה של 9,700 ש"ח לחודש מדובר ב-679 ש"ח לחודש. source: https://www.nevo.co.il/law_html/law00/84255.htm. why advanced: רלוונטי לעובד עם הפקדה עצמאית לפנסיה מעבר להפקדת המעסיק.

- [ ] משיכת קרן השתלמות לפני תום 6 שנים (משיכה שלא כדין). חיוב מס של 47%, אך לא על מלוא הצבירה: חלק העובד וחלק המעסיק שכבר נזקף כהכנסה פטורים מהמס הזה; אם שיעור המס השולי האמיתי של העובד נמוך מ-47%, ניתן לבקש החזר מס על ההפרש דרך טופס 135. source: https://pensuni.com/?p=2916. why advanced: requires reading the תלוש משיכה from the keren and comparing to marginal bracket.

- [ ] חובה בהגשת דוח שנתי לשכיר עם הכנסה גבוהה. שכיר עם הכנסות חריגות חייב בטופס 1301 ולא בטופס 135. source: https://www.bshcpa.co.il/%D7%93%D7%95%D7%97-%D7%A9%D7%A0%D7%AA%D7%99-%D7%A9%D7%9B%D7%99%D7%A8/. why advanced: skill must recognize this signal and refer the user to israeli-tax-returns.

- [ ] תיעוד דרוש לבקשת ההחזר. טפסי 106 מכל המעסיקים בשנה, אישורים מבטל"א על קצבאות מחליפות שכר (אבטלה/לידה/מילואים), קבלות סעיף 46 חתומות, אישורי ריבית/הפקדה מקופות גמל וביטוח, תעודת זהות + ספח, אישור ניהול חשבון בנק לזיכוי, אישור תושבות ביישוב מזכה. source: https://www.kolzchut.org.il/he/%D7%94%D7%97%D7%96%D7%A8_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94. why advanced: per-trigger checklist generation is one of the core skill outputs.

- [ ] תיאום מס מקוון בין מספר מעסיקים. distinguishing prospective adjustment (תיאום מס at gov.il. handles ongoing year) from retrospective refund (Form 135 / online system. handles closed past years). source: https://www.gov.il/he/service/tax-coordination-online. why advanced: users frequently conflate these.

- [ ] גירושין / הורה יחיד / משלם מזונות. additional credit points for single parent + deduction for paid alimony per Sections 64-66 ITO; documentation required = court judgment + bank transfers. source: https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94. why advanced: refund trigger most often missed when employer's 101 form is outdated post-divorce.

## Out of scope (explicit, with rationale)

- חובת הגשת טופס 1301 לבעלי הכנסות מעורבות/הון/יסף. separate obligated-filer track; the skill detects the signal and routes out. related skill: `israeli-tax-returns` handles it.
- חישוב ברוטו-נטו, פיענוח תלוש שכר חודשי, ניכויי בטל"א וקרן פנסיה. payroll mechanics, not annual reconciliation. related skill: `israeli-payroll-calculator` handles it.
- מיסוי אופציות לעובדים / RSU / מסלול 102. capital instrument tax. related skill: `israeli-stock-options-tax` handles it.
- מיסוי קריפטו ורווחי הון מנכסים דיגיטליים. separate reporting regime. related skill: `israeli-crypto-tax-reporter` handles it.
- מע"מ ודיווח מע"מ. relevant only to עוסק, not שכיר. related skill: `israeli-vat-reporting` handles it.
- מס שבח על מכירת דירה / רווח הון ממקרקעין. separate tax under חוק מיסוי מקרקעין. related skill: `israeli-tax-returns` covers cross-references.
- "סעיף 35 משכנתא לעולה חדש". Section 35 ITO governs נקודות זיכוי לעולה חדש / תושב חוזר ותיק (not mortgage interest). Mortgage-related tax benefits for olim flow through the new-immigrant credit-points regime. Excluded as a discrete trigger to avoid misinformation; oleh credit points handled under the נקודות זיכוי 2026 must-cover item above.

## Authoritative sources

- https://www.gov.il/he/service/itc135. Form 135 official page: who files, attachments, submission channels.
- https://www.gov.il/he/pages/sa300821-2. Online refund-for-employees system.
- https://www.kolzchut.org.il/he/%D7%94%D7%97%D7%96%D7%A8_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94. Kol-Zchut canonical guide; verify 6-year window per Section 160, statutory processing time, 4% interest + הצמדה.
- https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94. 2026 credit-point value 242 ₪/month, full category list.
- https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%9C%D7%95%D7%97%D7%9E%D7%99_%D7%9E%D7%99%D7%9C%D7%95%D7%90%D7%99%D7%9D. מילואים credit points per תיקון 283 (Section 39B).
- https://www.kolzchut.org.il/he/%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%91%D7%A9%D7%9C_%D7%AA%D7%A8%D7%95%D7%9E%D7%94_(%D7%A1%D7%A2%D7%99%D7%A3_46). 2026 donation ceiling 10,354,816 ₪ and minimum 207 ₪.
- https://www.kolzchut.org.il/he/%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%AA%D7%95%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A4%D7%A8%D7%99%D7%A4%D7%A8%D7%99%D7%94. 2026 official ישובים מוטבים list.
- https://www.kolzchut.org.il/he/%D7%94%D7%97%D7%96%D7%A8_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94. Section 9(5) disability exemption framework.
- https://www.kolzchut.org.il/he/%D7%98%D7%95%D7%A4%D7%A1_106. Form 106 fields explainer.
- https://pensuni.com/?p=827. 2026 pension/salary tax thresholds; sections 45א/47.
