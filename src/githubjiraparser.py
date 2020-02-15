import argparse
import re
from github import Github
from jira import JIRA, JIRAError

'''
python githubjiraparser.py -gr apache/activemq in order to parse apache active mq

python githubjiraparser.py -jp Cassandra -gr apache/cassandra

TODOs:

1. Receive all issues from jira for project:

2. Parse all issues and track comment metrics

3. Store all information in a csv file
'''

APACHE_JAVA_PROJECTS = [
    ".NET Ant Library",
    "Abdera",
    "Accumulo",
    "ACE",
    "ActiveMQ",
    "Airavata",
    "Ambari",
    "Anakia",
    "Ant",
    "AntUnit",
    "Any23",
    "Apex",
    "Archiva",
    "Aries",
    "Avro",
    "Axiom",
    "Axis2",
    "Beam",
    "Beehive",
    "Bigtop",
    "BookKeeper",
    "Brooklyn",
    "BVal",
    "Calcite",
    "Camel",
    "CarbonData",
    "Cassandra",
    "Cayenne",
    "Chainsaw",
    "Chemistry",
    "Chukwa",
    "Clerezza",
    "Click",
    "CloudStack",
    "Cocoon",
    "Commons BCEL",
    "Commons BeanUtils",
    "Commons BSF",
    "Commons Chain",
    "Commons CLI",
    "Commons Codec",
    "Commons Collections",
    "Commons Compress",
    "Commons Configuration",
    "Commons Daemon",
    "Commons DBCP",
    "Commons DbUtils",
    "Commons Digester",
    "Commons Discovery",
    "Commons EL",
    "Commons Email",
    "Commons Exec",
    "Commons FileUpload",
    "Commons Functor",
    "Commons HttpClient",
    "Commons IO",
    "Commons JCI",
    "Commons JCS",
    "Commons Jelly",
    "Commons JEXL",
    "Commons JXPath",
    "Commons Lang",
    "Commons Launcher",
    "Commons Logging",
    "Commons Math",
    "Commons Modeler",
    "Commons Net",
    "Commons OGNL",
    "Commons Pool",
    "Commons Proxy",
    "Commons RNG",
    "Commons SCXML",
    "Commons Validator",
    "Commons VFS",
    "Commons Weaver",
    "Compress Ant Library",
    "Continuum",
    "Cordova",
    "Crunch",
    "cTAKES",
    "Curator",
"CXF",
"Daffodil",
"DataFu",
"DeltaSpike",
"Derby",
"DeviceMap",
"DirectMemory",
"Directory",
"Directory Server",
"Directory Studio",
"Drill",
"ECS",
"Edgent",
"Empire - db",
"Etch",
"Excalibur",
"Falcon",
"Felix",
"Flink",
"Flume",
"Fluo",
"Fluo Recipes",
"Fluo YARN",
"FOP",
"Forrest",
"Fortress",
"FreeMarker",
"FtpServer",
"Geronimo",
"Giraph",
"Gora",
"Groovy",
"Guacamole",
"Hama",
"Harmony",
"HBase",
"Helix",
"Hive",
"Hivemind",
"HttpComponents Client",
"HttpComponents Core",
"Hudi",
"Ignite",
"Isis",
"Ivy",
"IvyDE",
"Jackrabbit",
"Jakarta Cactus",
"JAMES",
"jclouds",
"Jena",
"JMeter",
"JSPWiki",
"Karaf",
"Kerby",
"Knox",
"Lens",
"Lenya",
"Log4j 2",
"Lucene Core",
"Mahout",
"ManifoldCF",
"Marmotta",
"Maven",
"Maven Doxia",
"MetaModel",
"MINA",
"MRUnit",
"MyFaces",
"Nutch",
"ODE",
"OFBiz",
"Olingo",
"Oltu - Parent"
"OODT",
"Oozie",
"OpenJPA",
"OpenMeetings",
"OpenNLP",
"OpenWebBeans",
"ORC",
"ORO",
"Parquet",
"PDFBox",
"Phoenix",
"Pig",
"Pivot",
"PLC4X",
"POI",
"Polygene",
"Portals",
"Props Ant Library",
"Qpid",
"Rat",
"REEF",
"Regexp",
"River",
"Roller",
"Sandesha2",
"Santuario",
"Scout",
"ServiceMix",
"Shale",
"Shindig",
"Shiro",
"Sling",
"Solr",
"Spark",
"Spatial Information System",
"Sqoop",
"SSHD",
"Stanbol",
"Storm",
"Stratos",
"Struts",
"Synapse",
"Syncope",
"Tajo",
"Tapestry",
"Taverna",
"Tentacles",
"Texen",
"Tez",
"Thrift",
"Tika",
"Tiles",
"Tobago",
"Tomcat",
"TomEE",
"Torque",
"Turbine",
"Tuscany",
"UIMA",
"Velocity",
"Velocity DVSL",
"Velocity Tools",
"VSS Ant Library",
"VXQuery",
"Vysper",
"Whirr",
"Whisker",
"Wicket",
"Wink",
"Woden",
"Wookie",
"Xalan",
"Xerces",
"Xindice",
"XML Commons External",
"XML Commons Resolver",
"XML Graphics Commons",
"XMLBeans",
"Yetus",
"Zeppelin",
"ZooKeeper"
]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-gr", dest="gitrepo", required=False,
        help="github repository to parse")
    parser.add_argument(
        "-jp", dest="jiraproject", required=False,
        help="Jira project to parse")
    return parser.parse_args()


def parse_github(repository_title, prefix):
    github = Github()
    repository = github.get_repo(repository_title)
    pull_requests = repository.get_pulls()
    for pr in pull_requests:
        if prefix in pr.title:
            # note this is for the moment in order to increase performance
            return True
        # print(pr.title)
        # print(pr.state)
        # commits = pr.get_commits()
        # TODO: atm we require log in to parse commits because of rate limit of 60
        # TODO: check how many prs/commits have prefix included
        # TODO: store results in order to map issue num and pr/commit
    return False


def parse_apache_jira_projects():
    jira = JIRA('https://issues.apache.org/jira/')
    projects = jira.projects()
    for p in projects:
        # issues = jira.search_issues("project = %s" % p.name, maxResults=1)
        print(p.name)
        # print(issues.total)
    # i = 0
    # for issue in issues:
    #     i += 1
    #     issue_name = issue.key
    # issue_prefix = re.sub("\d+", "", issue_name)
    # issue_prefix = re.sub("-", "", issue_prefix)
    # print(i)
    return None


if __name__ == "__main__":
    args = parse_args()
    jira_issue_metrics = parse_apache_jira_projects()
