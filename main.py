import xml.etree.ElementTree as ET
import datetime
import argparse


def print_all_options():
    priced_itineraries = root1[1]
    for itin_numb, flights in enumerate(priced_itineraries):
        print(f'Itinerary {itin_numb + 1}\n')
        for i, elem in enumerate(flights):
            if i in [0, 1]:
                if i == 0:
                    print('The way there:')
                else:
                    print('The way back')
                for one_way_flights in elem:
                    for flight in one_way_flights:
                        d_date = flight[4].text.split('T')[0]
                        d_time = flight[4].text.split('T')[1]
                        a_date = flight[5].text.split('T')[0]
                        a_time = flight[5].text.split('T')[1]
                        print(f'{flight[2].text} - {flight[3].text}')
                        print(f'Departure:\t {d_date}, {d_time[:2]}:{d_time[2:]}')
                        print(f'Arrival:\t {a_date}, {a_time[:2]}:{a_time[2:]}')
                        print('Airline:\t', flight[0].text)
                        print()


def print_itinerary(itin_numb, root):
    priced_itineraries = root[1]
    for i, elem in enumerate(priced_itineraries[itin_numb]):
        if i in [0, 1]:
            if i == 0:
                print('The way there:')
            else:
                print('The way back')
            for one_way_flights in elem:
                for flight in one_way_flights:
                    d_date = flight[4].text.split('T')[0]
                    d_time = flight[4].text.split('T')[1]
                    a_date = flight[5].text.split('T')[0]
                    a_time = flight[5].text.split('T')[1]
                    print(f'{flight[2].text} - {flight[3].text}')
                    print(f'Departure:\t {d_date}, {d_time[:2]}:{d_time[2:]}')
                    print(f'Arrival:\t {a_date}, {a_time[:2]}:{a_time[2:]}')
                    print('Airline:\t', flight[0].text)
                    print()


def find_the_cheapest():
    priced_itineraries = root1[1]
    print(f'Price: {priced_itineraries[0][2][2].text}')
    print()
    print_itinerary(0, root1)


def find_the_most_expensive():
    priced_itineraries = root1[1]
    print(f'Price: {priced_itineraries[199][2][2].text}')
    print()
    print_itinerary(199, root1)


def find_duration(flights):
    duration = datetime.timedelta(0, 0, 0)
    for i, elem in enumerate(flights):
        if i in [0, 1]:
            for one_way_flights in elem:
                for flight in one_way_flights:
                    d_datetime = datetime.datetime.strptime(flight[4].text, '%Y-%m-%dT%H%M')
                    a_datetime = datetime.datetime.strptime(flight[5].text, '%Y-%m-%dT%H%M')
                    duration += a_datetime - d_datetime
    return str(duration)


def gather_durations_of_all():
    durations = []
    for itin_numb, flights in enumerate(root1[1]):
        duration = find_duration(flights)
        durations.append((itin_numb, str(duration)))
        durations.sort(key=lambda i: i[1])
    return durations


def the_most_optimal(durations):
    fastest = durations[:50]
    optimal = []
    for numb, duration in enumerate(fastest):
        optimal.append((duration[0], len(durations) - duration[0] + numb, duration[1]))
    return optimal


def find_differences():
    priced_itineraries1 = root1[1]
    priced_itineraries2 = root2[1]
    for itin_numb, itinerary in enumerate(priced_itineraries2):
        duration1 = find_duration(priced_itineraries1[itin_numb])
        duration2 = find_duration(itinerary)
        if duration1 > duration2:
            print(
                f'Itinerary #{itin_numb + 1} from the file RS_ViaOW.xml is faster than itinerary from the file RS_Via-3.xml')
            print(f'RS_Via-3.xml: {duration1}\t RS_ViaOW.xml: {duration2}')
        elif duration2 > duration1:
            print(
                f'Itinerary #{itin_numb + 1} from the file RS_Via-3.xml is faster than itinerary from the file RS_ViaOW.xml')
            print(f'RS_Via-3.xml: {duration1}\t RS_ViaOW.xml: {duration2}')
        else:
            print(f'Itineraries #{itin_numb + 1} from the files RS_Via-3.xml and RS_ViaOW.xml have the same duration')
            print(f'RS_Via-3.xml: {duration1}\t RS_ViaOW.xml: {duration2}')
        print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all', help='Show all options', action='store_true')
    parser.add_argument('-c', '--chp', help='Find the cheapest ticket ', action='store_true')
    parser.add_argument('-e', '--exp', help='Find the most expensive ticket ', action='store_true')
    parser.add_argument('-f', '--fst', help='Find the fastest ticket ', action='store_true')
    parser.add_argument('-s', '--slw', help='Find the slowest ticket ', action='store_true')
    parser.add_argument('-o', '--opt', help='Find the most optimal ticket ', action='store_true')
    parser.add_argument('-d', '--dif', help='Show the difference between requests ', action='store_true')
    args = parser.parse_args()

    if args.all:
        print_all_options()
    elif args.chp:
        find_the_cheapest()
    elif args.exp:
        find_the_most_expensive()
    elif args.fst:
        durations = gather_durations_of_all()
        print(f'The fastest itinerary: {durations[0][1]}')
        print_itinerary(durations[0][0], root1)
    elif args.slw:
        durations = gather_durations_of_all()
        print(f'The slowest itinerary: {durations[len(durations)-1][1]}')
        print_itinerary(durations[len(durations)-1][0], root1)
    elif args.opt:
        durations = gather_durations_of_all()
        optimal = the_most_optimal(durations)
        print(f'Duration: {sorted(optimal)[0][2]}')
        print(f'Price: {root1[1][sorted(optimal)[0][0]][2][2].text}')
        print()
        print_itinerary(sorted(optimal)[0][0], root1)
    elif args.dif:
        find_differences()


if __name__ == '__main__':
    tree1 = ET.parse('RS_Via-3.xml')
    root1 = tree1.getroot()

    tree2 = ET.parse('RS_ViaOW.xml')
    root2 = tree2.getroot()
    main()


