# Math & Physics Solver (one EXE)

Программа для решения базовых математических и физических задач в одном файле `.exe`.

## Что умеет

- **Математика**:
  - Решение квадратных уравнений `ax² + bx + c = 0`
  - Площадь и периметр прямоугольника
- **Физика**:
  - Сила `F = m · a`
  - Потенциальная энергия `E = m · g · h`

## Запуск в Python

```bash
python solver_app.py
```

## Сборка в один EXE (Windows)

1. Установить зависимости:

```bash
pip install -r requirements.txt
```

2. Собрать exe:

```bash
pyinstaller --noconfirm --onefile --windowed --name solver solver_app.py
```

3. Готовый файл будет в каталоге:

```text
dist/solver.exe
```

## Примечание

- На Linux/macOS получится бинарник для своей платформы.
- Для `solver.exe` нужно собирать на Windows (или в Windows CI/VM).
