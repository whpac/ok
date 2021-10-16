import random

with open('data.txt', 'w') as f:
    processor_count = random.randint(3, 15)
    process_count = random.randint(3 * processor_count, 100)

    print(f'Wygenerowano {process_count} procesów dla {processor_count} procesorów')

    f.write(f'{processor_count}\n{process_count}\n')
    for i in range(process_count):
        f.write(str(random.randint(1, 50)) + '\n')