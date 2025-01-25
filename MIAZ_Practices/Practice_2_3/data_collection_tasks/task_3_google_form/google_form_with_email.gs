/**
 * Створює Google Форму для збору інформації (ім'я, дата, відділ, email)
 * і зберігає посилання на форму в таблицю.
 * (Мова: Google Apps Script)
 */
function createInformationForm() {
  try {
    // Створюємо нову форму
    var form = FormApp.create('Інформаційна форма');

    // Додаємо опис до форми
    form.setDescription('Будь ласка, заповніть цю форму, надавши необхідну інформацію.');

    // Додаємо питання про електронну пошту (обов'язкове)
    var emailItem = form.addTextItem()
      .setTitle('Ваша електронна пошта')
      .setRequired(true);

    // Валідація електронної пошти (розширена перевірка)
    var emailValidation = FormApp.createTextValidation()
      .setHelpText('Введіть дійсну електронну адресу.')
      .requireTextMatchesPattern('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$') // Покращений регулярний вираз для перевірки email
      .build();
    emailItem.setValidation(emailValidation);

    // Додаємо питання про ім'я
    form.addTextItem()
      .setTitle('Ваше ім\'я')
      .setRequired(true);

    // Додаємо питання про дату
    form.addDateItem()
      .setTitle('Дата')
      .setRequired(true);

    // Додаємо питання про відділ
    form.addTextItem()
      .setTitle('Відділ')
      .setRequired(true);

    // Отримуємо опубліковане посилання на форму
    var formUrl = form.getPublishedUrl();

    // Отримуємо ID форми
    var formId = form.getId();

    // Отримуємо конкретний аркуш за його ім'ям
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Відповіді');

    // Перевірка наявності аркуша
    if (sheet == null) {
      throw new Error("Аркуш з ім'ям 'Відповіді' не знайдено.");
    }

    // Шукаємо останній заповнений рядок у першому стовпці
    var lastRow = sheet.getLastRow();

    // Вставляємо дані в таблицю (додаємо заголовок, якщо це перший запис)
    if (lastRow === 0) {
      sheet.getRange(1, 1).setValue("Назва форми");
      sheet.getRange(1, 2).setValue("ID форми");
      sheet.getRange(1, 3).setValue("Посилання на форму");
      sheet.getRange(1, 1, 1, 3).setHorizontalAlignment("center").setFontWeight("bold");
      lastRow = 1;
    }

    // Вставляємо дані в таблицю
    sheet.getRange(lastRow + 1, 1).setValue("Інформаційна форма");
    sheet.getRange(lastRow + 1, 2).setValue(formId);
    sheet.getRange(lastRow + 1, 3).setValue(formUrl);

    // Встановлюємо ширину стовпців
    sheet.setColumnWidth(1, 200);
    sheet.setColumnWidth(2, 150);
    sheet.setColumnWidth(3, 400);

    Logger.log('Посилання на форму: ' + formUrl);
    Logger.log('ID форми: ' + formId);
    Logger.log('Дані збережено в таблиці.');

  } catch (error) {
    Logger.log('Сталася помилка: ' + error.toString());
    SpreadsheetApp.getActiveSpreadsheet().toast('Сталася помилка при створенні форми: ' + error.toString(), 'Помилка', -1);
  }
}