# PythonHomeWork

Программа реализует симуляцию простых физических моделей и системы управления с помощью ПИД контроллера. Варианты физического воздействия прописываются пользователем как плагины и не требуеют вмешаетльства в архитектуру исходного кода основной программы. Программы рализующие физическое воздействие возвращают значение как реузльтат выполнения лямбда функции, а декоратор используется для получения названия интересующего пользователя плагина. 

Интерактивный интерфейс использующий слайдеры ползволяют наблюдать измнение поведения модели в зависимости от коэффициентов ПИД контроллера
