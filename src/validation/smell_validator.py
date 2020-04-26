import operator

CYCLIC_HEADER = "**************** CYCLIC DEPENDENCIES ****************"


class SmellValidator(object):

    def validate_smell(self, validation_smells, existing_smells):
        report = list([CYCLIC_HEADER])
        # check cyclic dependencies
        cyclic_dependencies_report = dict()
        for smell in validation_smells.cyclic_dependencies:
            match_list = dict()
            for existing_smell in existing_smells.cyclic_dependencies:
                matches = 0
                for component in smell.participating_components:
                    match = False
                    for existing_component in existing_smell.participating_components:
                        if component.name == existing_component.name:
                            match = True
                    if match:
                        matches += 1
                if matches >= 2:
                    match_list[existing_smell.id] = matches
                # TODO: atm the first cycle with the mst matches is printed --> refactor in order to provide information about all cycles
                # print(match_list)
                # key_s = max(match_list.items(), key=operator.itemgetter(1))
                # print(key_s)
                # key = key_s[0]
            key = -1 if len(match_list) == 0 else max(match_list.items(), key=operator.itemgetter(1))[0]
            cyclic_dependencies_report[smell.id] = {
                "matched": 1 if len(match_list) > 0 else 0,
                "similar_cycles": len(match_list),
                "closest_match_id": key,
                "closest_match_num": 0 if key == -1 else match_list[key]
            }
        total_matches = sum([v["matched"] for k,v in cyclic_dependencies_report.items()])
        report.append("There are %d cyclic dependencies and %d confirmed cycles in this version!" % (len(cyclic_dependencies_report), total_matches))
        for smell_id, smell in cyclic_dependencies_report.items():
            report.append("Id %s \t %d \t similar confirmed cycles! \t" \
                          "Closest existing smell: Id \t %d with \t %d matching components!" \
                          % (smell_id, smell["similar_cycles"], smell["closest_match_id"], smell["closest_match_num"]))
        return report

