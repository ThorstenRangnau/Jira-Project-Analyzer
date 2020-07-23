import argparse
import csv
import re

from architectural_smells.smell import Version, CyclicDependency, UnstableDependency, HubLikeDependency
from datetime import datetime
from treelib import Node, Tree

from issue_information_aggregation import read_issue_information

DATE = 'birth_day'
DATE_FORMATTER_IMPORT = '%Y-%m-%d %H:%M:%S'
DATE_FORMATTER_PARAM = '%Y-%m-%d'
COMMIT_SHA = 'commit_sha'
ELEMENTS = 'affected_elements'
SMELL_TYPE = 'smell_type'
UNIQUE_SMELL_ID = 'unique_smell_id'
BIRTH_DAY = 'birth_day'
SIZE = 'size'
CYCLIC_DEPENDENCY = 'cyclic_dependency'
UNSTABLE_DEPENDENCY = 'unstable_dependency'
HUBLIKE_DEPENDENCY = 'hublike_dependency'
SHAPE = 'shape'
INSTABILITY_GAP = 'instability_gap'
DOUD = 'doud'
AVRG_PATH_LENGTH = 'avrg_inner_path_length'
AFFECTED_CLASS_RATIO = 'affected_class_ratio'
CD_KEY = 'CYCLIC_DEPENDENCY'
UD_KEY = 'UNSTABLE_DEPENDENCY'
HD_KEY = 'HUBLIKE_DEPENDENCY'
M1 = 'm1'
M2 = 'm2'


def create_smell(row):
    version = row[COMMIT_SHA]
    smell_type = row[SMELL_TYPE]
    unique_smell_id = int(row[UNIQUE_SMELL_ID])
    birth_day = datetime.strptime(row[BIRTH_DAY], DATE_FORMATTER_IMPORT)
    affected_elements = re.findall("\'(.*?)\'", row[ELEMENTS])
    size = row[SIZE]
    if smell_type == CYCLIC_DEPENDENCY:
        return CyclicDependency(unique_smell_id, birth_day, version, affected_elements, size, row[SHAPE])
    if smell_type == UNSTABLE_DEPENDENCY:
        return UnstableDependency(unique_smell_id, birth_day, version, affected_elements, size, row[INSTABILITY_GAP],
                                  row[DOUD])
    if smell_type == HUBLIKE_DEPENDENCY:
        return HubLikeDependency(unique_smell_id, birth_day, version, affected_elements, size, row[AVRG_PATH_LENGTH],
                                 row[AFFECTED_CLASS_RATIO])


def import_smells(directory, name):
    total = discarded_smells_by_date = smell_instances = 0
    smells = dict()
    smells[CYCLIC_DEPENDENCY] = list()
    smells[UNSTABLE_DEPENDENCY] = list()
    smells[HUBLIKE_DEPENDENCY] = list()
    with open('%s/%s_smells_by_version.csv' % (directory, name), mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            total += 1
            smell_instances += 1
            smell = create_smell(row)
            if isinstance(smell, CyclicDependency):
                smells[CYCLIC_DEPENDENCY].append(smell)
            if isinstance(smell, UnstableDependency):
                smells[UNSTABLE_DEPENDENCY].append(smell)
            if isinstance(smell, HubLikeDependency):
                smells[HUBLIKE_DEPENDENCY].append(smell)
    return smells, total, discarded_smells_by_date, smell_instances


def same_elements(affected_elements1, affected_elements2):
    for element in affected_elements1:
        if element not in affected_elements2:
            return False
    return True


def detect_duplicated_smell(smell, unique_smells):
    for k, v in unique_smells.items():
        if same_elements(smell.get_affected_elements(), v.get_affected_elements()):
            return True, k
    return False, -1


def new_smell_is_older(smell, old_smell):
    if smell.birth_day < old_smell.birth_day:
        return True
    return False


def filter_duplicated_smells(smells_types):
    unique_smells_types = dict()
    for smell_type, smells in smells_types.items():
        print('Parse %s' % smell_type)
        unique_smells = dict()
        unique_smell_idx = 0
        for smell in smells:
            # for initial iteration
            if not unique_smells:
                unique_smells[unique_smell_idx] = smell
                unique_smell_idx += 1
                continue
            duplicated, idx = detect_duplicated_smell(smell, unique_smells)
            if duplicated:
                if new_smell_is_older(smell, unique_smells[idx]):
                    unique_smells[idx] = smell
            else:
                unique_smells[unique_smell_idx] = smell
                unique_smell_idx += 1
        unique_smells_types[smell_type] = unique_smells
    return unique_smells_types


def write_unique_smells_to_csv(directory, name, smells_sorted_by_version):
    with open('%s/%s_filtered_smells_by_version.csv' % (directory, name), mode='w') as csv_file:
        fieldnames = ['commit_sha',
                      'smell_type',
                      'unique_smell_id',
                      'birth_day',
                      'size',
                      'shape',
                      'instability_gap',
                      'doud',
                      'avrg_inner_path_length',
                      'affected_class_ratio',
                      'affected_elements']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for commit_sha, version in smells_sorted_by_version.items():
            for smell_type, smells in version.smells_by_type.items():
                for smell_id, smell in smells.items():
                    writer.writerow({
                        'commit_sha': commit_sha,
                        'smell_type': smell_type.lower(),
                        'unique_smell_id': smell_id,
                        'birth_day': smell.birth_day,
                        'size': smell.size,
                        'shape': smell.shape if isinstance(smell, CyclicDependency) else ' ',
                        'instability_gap': smell.instability_gap if isinstance(smell, UnstableDependency) else ' ',
                        'doud': smell.doud if isinstance(smell, UnstableDependency) else ' ',
                        'avrg_inner_path_length': smell.avrg_internal_path_length if isinstance(smell,
                                                                                                HubLikeDependency) else ' ',
                        'affected_class_ratio': smell.affected_classes_ratio if isinstance(smell,
                                                                                           HubLikeDependency) else ' ',
                        'affected_elements': smell.get_affected_elements()
                    })


def sort_smells_by_version(types_smells):
    versions = dict()
    for smell_type, smells in types_smells.items():
        for idx, smell in smells.items():
            commit_sha = smell.version
            if commit_sha not in versions:
                versions[commit_sha] = Version(commit_sha)
            versions[commit_sha].add_smell(smell)
            versions[commit_sha].date = smell.birth_day
    return versions


def convert_to_list_and_sort(smells):
    versions = list()
    for commit_sha, version in smells.items():
        versions.append(version)
    versions.sort(key=lambda v: v.date)
    return versions


def check_first_date(comparison_date, first, last):
    earliest_date = first
    latest_date = last
    if first is None or last is None:
        return comparison_date, comparison_date
    if comparison_date < first:
        earliest_date = comparison_date
    if comparison_date > last:
        latest_date = comparison_date
    return earliest_date, latest_date


def write_versions_csv(directory, name, smells_sorted_by_version):
    total_cd = total_ud = total_hd = 0
    first_date = last_date = None
    with open('%s/%s_filtered_smells_aggregated_by_version.csv' % (directory, name), mode='w') as csv_file:
        fieldnames = ['id',
                      'commit_sha',
                      'date',
                      'cyclic_dependencies',
                      'unstable_dependencies',
                      'hub_like_dependencies']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for idx, version in enumerate(smells_sorted_by_version):
            total_cd += len(version.smells_by_type[CD_KEY])
            total_ud += len(version.smells_by_type[UD_KEY])
            total_hd += len(version.smells_by_type[HD_KEY])
            first_date, last_date = check_first_date(version.get_date(), first_date, last_date)
            writer.writerow({
                'id': idx + 1,
                'commit_sha': version.commit_sha,
                'date': version.get_date(),
                'cyclic_dependencies': len(version.smells_by_type[CD_KEY]),
                'unstable_dependencies': len(version.smells_by_type[UD_KEY]),
                'hub_like_dependencies': len(version.smells_by_type[HD_KEY])
            })
    with open('%s/%s_filtered_aggregated_metrics.csv' % (directory, name), mode='w') as csv_file:
        fieldnames = ['total_versions',
                      'from',
                      'till',
                      'total_smells',
                      'total_cyclic_dependencies',
                      'total_unstable_dependencies',
                      'total_hublike_dependencies']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            'total_versions': len(smells_sorted_by_version),
            'from': first_date,
            'till': last_date,
            'total_smells': total_cd + total_ud + total_hd,
            'total_cyclic_dependencies': total_cd,
            'total_unstable_dependencies': total_ud,
            'total_hublike_dependencies': total_hd
        })


def sort_smells_by_type_and_components(types_smells):
    smells_by_type_by_components = dict()
    for smell_type, smells in types_smells.items():
        smell_types = list()
        for idx, smell in smells.items():
            smell_types.append(smell)
        smell_types.sort(key=lambda s: str(s.get_affected_elements()), reverse=True)
        smells_by_type_by_components[smell_type] = smell_types
    return smells_by_type_by_components


def write_smells_by_component(directory, name, smells_components):
    with open('%s/%s_filtered_smells_by_components.csv' % (directory, name), mode='w') as csv_file:
        fieldnames = ['id',
                      'date',
                      'elements']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for smell_types, smells in smells_components.items():
            writer.writerow({'id': smell_types})
            for smell in smells:
                writer.writerow({
                    'id': smell.unique_smell_id,
                    'date': smell.birth_day,
                    'elements': smell.get_affected_elements()
                })
            writer.writerow({})


def align_smell_variations_by_smell(smells):
    '''
    :param smells:
    :return: { smell_id: --> [list of smell variations] }
    '''
    origin_smell_comp_1 = origin_smell_comp_2 = None
    variations_by_smell = dict()
    smell_id = 0
    for smell in smells:
        if len(smell.get_affected_elements()) == 1:
            continue
        if origin_smell_comp_1 is None and origin_smell_comp_2 is None:
            # initial loop
            origin_smell_comp_1, origin_smell_comp_2 = smell.get_affected_elements()[0], smell.get_affected_elements()[
                1]
            variations_by_smell[smell_id] = list()
            variations_by_smell[smell_id].append(smell)
            smell_id += 1
            continue
        comp_1, comp_2 = smell.get_affected_elements()[0], smell.get_affected_elements()[1]
        if comp_1 == origin_smell_comp_1 and comp_2 == origin_smell_comp_2:
            # same smell
            variations_by_smell[smell_id - 1].append(smell)
        else:
            # new smell
            origin_smell_comp_1, origin_smell_comp_2 = comp_1, comp_2
            variations_by_smell[smell_id] = list()
            variations_by_smell[smell_id].append(smell)
            smell_id += 1
    return variations_by_smell


def find_root_smell_variation(smell_variations):
    earliest = None
    for smell in smell_variations:
        if earliest is None:
            # initial loop
            earliest = smell
            continue
        if smell.birth_day < earliest.birth_day:
            earliest = smell
    return earliest


def calculate_m1(smell_variation, node):
    diff = len(smell_variation.get_affected_elements()) - len(node.data.get_affected_elements()) - 1
    return abs(diff)


def coverage(smell_variation, node):
    count = 0
    for element in node.data.get_affected_elements():
        if element in smell_variation.get_affected_elements():
            count += 1
    return count


def calculate_m2(smell_variation, node):
    c = coverage(smell_variation, node)
    return c / len(node.data.get_affected_elements())


def compare_metrics(metrics_by_node, min_m1, max_m2):
    both_best = list()
    one_best = list()
    for identifier, metrics in metrics_by_node.items():
        m1 = m2 = False
        if metrics[M1] == min_m1:
            m1 = True
        if metrics[M2] == max_m2:
            m2 = True
        if m1 and m2:
            # is in both the best
            both_best.append(identifier)
        elif m1 or m2:
            one_best.append(identifier)
    if len(both_best) > 1:
        oldest = None
        oldest_node = None
        for node_name in both_best:
            date = metrics_by_node[node_name][BIRTH_DAY]
            if oldest is None:
                # initial loop
                oldest = date
                oldest_node = node_name
                continue
            if date < oldest:
                oldest = date
                oldest_node = node_name
        return oldest_node
    if len(both_best) == 1:
        return both_best[0]
    if len(one_best) > 1:
        youngest = None
        youngest_node = None
        for node in one_best:
            birth_date = metrics_by_node[node][BIRTH_DAY]
            if youngest is None:
                # initial loop
                youngest = birth_date
                youngest_node = node
                continue
            if youngest < birth_date:
                youngest = birth_date
                youngest_node = node
        return youngest_node
    if len(one_best) == 1:
        return one_best[0]


def decide_parent_node(smell_variation, nodes):
    m1_metrics = list()
    m2_metrics = list()
    metrics_by_node = dict()
    for node in nodes:
        m1 = calculate_m1(smell_variation, node)
        m2 = calculate_m2(smell_variation, node)
        m1_metrics.append(m1)
        m2_metrics.append(m2)
        metrics_by_node[node.identifier] = dict()
        metrics_by_node[node.identifier][M1] = m1
        metrics_by_node[node.identifier][M2] = m2
        metrics_by_node[node.identifier][BIRTH_DAY] = node.data.birth_day
    min_m1 = min(m1_metrics)
    max_m2 = max(m2_metrics)
    return compare_metrics(metrics_by_node, min_m1, max_m2)


def create_smell_evolution_trees(variations_by_smell, start_at):
    smell_ids_tree = dict()
    start = datetime.strptime(start_at, DATE_FORMATTER_PARAM) if start_at is not None else None
    for smell_id, smell_variations in variations_by_smell.items():
        root = find_root_smell_variation(smell_variations)
        if root is None:
            # no smell detected at all
            continue
        if start is not None and root.birth_day < start:
            # smell is too old
            continue
        # create tree
        tree = Tree()
        # set root as root node for tree
        tree.create_node('Root', 'root', data=root)
        # remove root from smell list to ignore it and sort remaining list by date
        smell_variations.remove(root)
        smell_variations.sort(key=lambda s: s.birth_day)
        for idx, smell_variation in enumerate(smell_variations):
            smell_identifier = str(idx + 1)
            nodes = tree.all_nodes()
            parent_name = decide_parent_node(smell_variation, nodes)
            tree.create_node('Smell-%s' % smell_identifier, 'smell_%s' % smell_identifier, parent=parent_name,
                             data=smell_variation)
        # tree.show()
        smell_ids_tree[smell_id] = tree
    return smell_ids_tree


def filter_evolved_smells(smells_components, start_at):
    smell_type_trees = dict()
    for smell_type, smells in smells_components.items():
        variations_by_smell = align_smell_variations_by_smell(smells)
        print('Without date filtering: %d %s instances' % (len(variations_by_smell), smell_type))
        # check when the smell was created here!
        trees_by_smell_id = create_smell_evolution_trees(variations_by_smell, start_at)
        print('Smell type %s - %d smells' % (smell_type, len(trees_by_smell_id)))
        smell_type_trees[smell_type] = trees_by_smell_id
    return smell_type_trees


def write_smell_evolution(directory, name, smell_type_smell_id_tree, commit_sha_issues):
    with open('%s/%s_smell_tree.csv' % (directory, name), mode='w') as csv_file:
        fieldnames = ['smell_id',
                      'root',
                      'node_name',
                      'parent',
                      'issue_key',
                      'commit_sha',
                      'birth_date',
                      'issue_type',
                      'components']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for smell_type, tree_by_id in smell_type_smell_id_tree.items():
            # some space to separate smell types
            writer.writerow({})
            writer.writerow({
                'smell_id': smell_type
            })
            writer.writerow({})
            # write smells by smell id
            for smell_id, tree in tree_by_id.items():
                # for root
                root = tree.get_node('root')
                root_smell = root.data
                writer.writerow({
                    'smell_id': smell_id,
                    'root': root.tag,
                    'node_name': ' ',
                    'parent': ' ',
                    'issue_key': commit_sha_issues[root_smell.version].issue_key if root_smell.version in commit_sha_issues else "No key",
                    'commit_sha': root_smell.version,
                    'birth_date': root_smell.birth_day,
                    'issue_type': commit_sha_issues[root_smell.version].issue_type if root_smell.version in commit_sha_issues else "No Type",
                    'components': root_smell.get_affected_elements()
                })
                writer.writerow({})
                for node in tree.all_nodes():
                    if node.identifier == 'root':
                        continue
                    node_smell = node.data
                    writer.writerow({
                        'smell_id': smell_id,
                        'root': ' ',
                        'node_name': node.tag,
                        'parent': node.bpointer,
                        'issue_key': commit_sha_issues[node_smell.version].issue_key if node_smell.version in commit_sha_issues else "No key",
                        'commit_sha': node_smell.version,
                        'birth_date': node_smell.birth_day,
                        'issue_type': commit_sha_issues[node_smell.version].issue_type if node_smell.version in commit_sha_issues else "No type",
                        'components': node_smell.get_affected_elements()
                    })
                writer.writerow({})


def transform_to_dict(issues):
    commit_issue = dict()
    for version in issues:
        if version.commit_sha in commit_issue:
            print('duplicated commit')
        commit_issue[version.commit_sha] = version
    return commit_issue


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", dest="directory", required=True,
        help="Path to input file -- needs to be an output of ASTracker")
    parser.add_argument(
        "-n", dest="name", required=True,
        help="Project name")
    parser.add_argument(
        "-s", dest="start_at", required=False, default=None,
        help="Considers only package level architectural smells!")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    smells_by_type, tot, discarded, instances = import_smells(args.directory, args.name)
    print("Total: %d, Discarded: %d, Imported: %d" % (tot, discarded, instances))
    filtered_smells_by_type = filter_duplicated_smells(smells_by_type)
    cd = len(filtered_smells_by_type[CYCLIC_DEPENDENCY])
    ud = len(filtered_smells_by_type[UNSTABLE_DEPENDENCY])
    hd = len(filtered_smells_by_type[HUBLIKE_DEPENDENCY])
    print('Remaining smells: %d, cyclic: %d, unstable: %d, hublike: %d' % ((cd + ud + hd), cd, ud, hd))
    # sort smells and write sorted by smell type and component
    smells_by_component = sort_smells_by_type_and_components(filtered_smells_by_type)
    # write_smells_by_component(args.directory, args.name, smells_by_component)
    trees_by_smell_type = filter_evolved_smells(smells_by_component, args.start_at)
    issue_information = read_issue_information(args.directory, args.name, None)
    issues_by_key = transform_to_dict(issue_information)
    write_smell_evolution(args.directory, args.name, trees_by_smell_type, issues_by_key)

    # smells_by_version = sort_smells_by_version(filtered_smells_by_type)
    # write_unique_smells_to_csv(args.directory, args.name, smells_by_version)
    # smelly_versions = convert_to_list_and_sort(smells_by_version)
    # write_versions_csv(args.directory, args.name, smelly_versions)
