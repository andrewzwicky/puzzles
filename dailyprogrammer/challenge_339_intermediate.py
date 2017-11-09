def recursive_rental_max(rentals,
                         planned_rentals=(),
                         max_planned_rentals=(),
                         max_rental_days=0):
    last_planned_rental_start = 0 if len(planned_rentals) == 0 else planned_rentals[-1].start
    
    for rental in rentals:
        # planned_rentals should be in sorted order, so only check rental
        # periods starting after the last planned rental.
        if rental not in planned_rentals and rental.start > last_planned_rental_start:
            fits = True
            for planned_rental in planned_rentals:
                if set(rental) & set(planned_rental):
                    # If the rental overlaps with any existing rental period,
                    # break and move on to the next rental period.
                    fits = False
                    break

            if fits:
                new_planned_rentals = planned_rentals + (rental,)
                new_planned_days = sum([t.stop-t.start for t in new_planned_rentals])
                existing_max_days = sum([t.stop-t.start for t in max_planned_rentals])
                
                new_planned_is_longer = len(new_planned_rentals) > len(max_planned_rentals)
                new_planned_is_equal = len(new_planned_rentals) == len(max_planned_rentals)
                new_planned_has_more_days = new_planned_days > existing_max_days
                
                
                if new_planned_is_longer or (new_planned_is_equal and new_planned_has_more_days):
                    max_planned_rentals = new_planned_rentals

                max_planned_rentals = recursive_rental_max(rentals,
                                                           new_planned_rentals,
                                                           max_planned_rentals,
                                                           max_rental_days)
    return max_planned_rentals

starts = "1 10 5 12 13 40 30 22 70 19"
ends= "23 12 10 29 25 66 35 33 100 65"

rentals = [range(int(start), int(end)+1) for start,end in zip(starts.split(" "), ends.split(" "))]
rentals.sort(key = lambda x: x.start)
    
rentals = recursive_rental_max(rentals)
print([(t.start, t.stop-1) for t in rentals])
