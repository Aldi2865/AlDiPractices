// main.js

// Функція для малювання вісімки, що адаптується до розміру canvas
function drawFigureEight() {
    // Отримуємо доступ до елемента canvas
    const canvas = document.getElementById('graph1'); // Використовуємо ID з вашого HTML
    // Перевіряємо, чи елемент існує
    if (!canvas) {
        console.error('Елемент canvas з ID "graph1" не знайдено!');
        return; // Виходимо, якщо canvas не знайдено
    }

    // Отримуємо 2D контекст для малювання
    const ctx = canvas.getContext('2d');
    // Перевіряємо, чи вдалося отримати контекст
    if (!ctx) {
        console.error('Не вдалося отримати 2D контекст для canvas.');
        return;
    }

    // --- Динамічні параметри малювання ---
    // Важливо: отримуємо реальні розміри елемента canvas, які можуть бути змінені CSS
    // Атрибути canvas.width/height визначають роздільну здатність, а не відображуваний розмір.
    // Для простоти, припустимо, що CSS правильно керує розміром,
    // але в складніших випадках може знадобитися оновлювати width/height атрибути
    // відповідно до clientWidth/clientHeight та перемальовувати.
    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;

    // Визначаємо меншу сторону для розрахунку масштабу, щоб вісімка влізла
    const minDimension = Math.min(canvasWidth, canvasHeight);

    // Розраховуємо радіус відносно меншої сторони (наприклад, 1/4)
    // Віднімаємо невеликий відступ, щоб лінія не торкалася країв
    const padding = 10; // Відступ від країв
    const availableSpace = minDimension - padding * 2;
    // Радіус одного кола приблизно 1/4 доступного простору
    const radius = Math.max(10, availableSpace / 4); // Мінімальний радіус 10

    // Розраховуємо товщину лінії відносно радіуса (наприклад, 1/6 радіуса)
    const lineWidth = Math.max(2, radius / 6); // Мінімальна товщина 2

    // Розраховуємо вертикальне зміщення центрів кіл відносно радіуса
    const verticalOffset = radius / 1.5;

    // Центр canvas
    const centerX = canvasWidth / 2;
    const centerY = canvasHeight / 2;

    const lineColor = 'royalblue'; // Колір лінії

    // --- Налаштування лінії ---
    ctx.lineWidth = lineWidth; // Встановлюємо товщину
    ctx.strokeStyle = lineColor; // Встановлюємо колір

    // Очищення canvas перед малюванням
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);

    // --- Малювання вісімки ---
    ctx.beginPath(); // Починаємо новий шлях

    // Малюємо верхнє коло вісімки
    // Перевіряємо, чи центри кіл не виходять за межі canvas
    const topCircleY = centerY - verticalOffset;
    const bottomCircleY = centerY + verticalOffset;

    // Малюємо, тільки якщо кола вміщаються
    if (topCircleY - radius >= 0 && bottomCircleY + radius <= canvasHeight) {
         ctx.arc(centerX, topCircleY, radius, 0, 2 * Math.PI);
         // Малюємо нижнє коло вісімки
         ctx.arc(centerX, bottomCircleY, radius, 0, 2 * Math.PI);
    } else {
        console.warn("Canvas занадто малий для малювання вісімки з поточними пропорціями.");
        // Можна намалювати щось інше або нічого не малювати
        // Наприклад, намалюємо одне коло по центру
        const singleRadius = Math.max(5, availableSpace / 2 - lineWidth / 2);
        if (singleRadius > 0) {
             ctx.arc(centerX, centerY, singleRadius, 0, 2 * Math.PI);
        }
    }


    // Застосовуємо малювання контуру
    ctx.stroke();

    console.log('Вісімку намальовано в main.js з адаптивними розмірами!');
}

// --- Виклик функції малювання ---
// Додамо обробник зміни розміру вікна для перемальовування
// (це базовий приклад, для складних випадків може знадобитися ResizeObserver)
let resizeTimeout;
window.addEventListener('resize', () => {
    // Використовуємо debounce, щоб не перемальовувати занадто часто
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        // Важливо: Оновити атрибути width/height canvas перед перемальовуванням,
        // якщо його розмір на сторінці змінився!
         const canvas = document.getElementById('graph1');
         if (canvas) {
             // Оновлюємо роздільну здатність відповідно до CSS розміру
             // Це також очистить canvas
             canvas.width = canvas.clientWidth;
             canvas.height = canvas.clientHeight;
             drawFigureEight(); // Перемальовуємо
         }
    }, 250); // Затримка 250 мс
});


// Переконуємося, що DOM повністю завантажений перед першим малюванням
if (document.readyState === 'loading') { // Ще завантажується
    document.addEventListener('DOMContentLoaded', () => {
         const canvas = document.getElementById('graph1');
         if (canvas) {
             canvas.width = canvas.clientWidth;
             canvas.height = canvas.clientHeight;
             drawFigureEight();
         }
    });
} else { // DOM вже завантажений
     const canvas = document.getElementById('graph1');
     if (canvas) {
         canvas.width = canvas.clientWidth;
         canvas.height = canvas.clientHeight;
         drawFigureEight();
     }
}
