/**
 * Створює Google Форму для збору інформації (ім'я, дата, відділ)
 * і зберігає посилання на форму в таблицю.
 * (Мова: Google Apps Script)
 */
function createInformationForm() {
  // Створюємо нову форму
  var form = FormApp.create('Інформаційна форма');

  // Додаємо опис до форми
  form.setDescription('Будь ласка, заповніть цю форму, надавши необхідну інформацію.');

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

  // Отримуємо активний аркуш
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

  // Шукаємо останній заповнений рядок у першому стовпці
  var lastRow = sheet.getLastRow();

  // Вставляємо дані в таблицю
  sheet.getRange(lastRow + 1, 1).setValue("Інформаційна форма");
  sheet.getRange(lastRow + 1, 2).setValue(formId);
  sheet.getRange(lastRow + 1, 3).setValue(formUrl);

  Logger.log('Посилання на форму: ' + formUrl);
  Logger.log('ID форми: ' + formId);
  Logger.log('Дані збережено в таблиці.');
}