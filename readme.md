# Игра про танки на питоне
## Управление
### Игра
Стартуем файлом editor.py, как ни странно.
- R - начать новую игру / сбросить
- J - подключить геймпады

Остальное с геймпада.
###  Редактор
- L - загрузить уровень (пока один)
- S - сохранить уровень (пока в один и тот же файл)
- B - кисть (пока ни хрена не отображается текущая)
- F - сетка и технические спрайты (респавны)
- W - начать игру на потестить не сохраненный уровень
- ЛКМ - добавить блок
- ПКМ - убрать блок
- СКМ - запустить тестового дебила на уровень
### Режимы игры
См. config.py
### Элементы
- blocks - блоки уровня
- tanks - танки разного рода (есть тудухи)
- controllers - контроллеры танков (автомат, геймпад)
- tank_shell - снаряд танка (много тудух)
- level - собстна уровень и хранилище блоков да танков
- layers - слой уровня, не идеален
- effects - спецэффекты, пока только взрыв