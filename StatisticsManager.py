import matplotlib.pyplot as plt

days_of_week = [
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье'
]

hours = [h for h in range(24)]


def update_all_diagrams(database_manager, logger):
    for day in range(7):
        statistics = database_manager.select_day_statistics(day)
        logger.debug(statistics)
        avg_visits_count = {}
        for _, hour, visits_count, weeks_count in statistics:
            avg_visits_count[hour] = visits_count
        logger.debug(avg_visits_count)
        update_diagram(day, [avg_visits_count[h] for h in range(24)], logger)


def update_diagram(week_day, avg_visits_count, logger):
    width = 0.35
    fig, ax = plt.subplots()
    ax.bar(hours, avg_visits_count, width)
    ax.set_ylabel('Среднее число посещений')
    ax.set_ylim([0, None])
    ax.set_xlabel('Время, ч')
    ax.set_title(days_of_week[week_day])

    plt.savefig('config/images/' + str(week_day) + '.png')

    logger.debug(f'updated diagram for day {week_day}')
