import os
import requests
from collections import defaultdict


def delete_dir(path):
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            delete_dir(full_path)
    os.rmdir(path)


def reset_dir(path):
    if os.path.exists(path):
        delete_dir(path)
    os.mkdir(path)


def run_me(source_path, hostname, port):
    route_template = hostname + ":" + port + "/v1/letters/{0}/letter?icn={1}"
    pdf_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pdfs")
    reset_dir(pdf_dir)
    print(pdf_dir)
    letter_types = [
          "BENEFIT_SUMMARY",
          "BENEFIT_SUMMARY_DEPENDENT",
          "BENEFIT_VERIFICATION",
          "CIVIL_SERVICE",
          "COMMISSARY",
          "PROOF_OF_SERVICE",
          "SERVICE_VERIFICATION",
          "MEDICARE_PARTD",
          "MINIMUM_ESSENTIAL_COVERAGE"
    ]
    [os.mkdir(os.path.join(pdf_dir, letter_type)) for letter_type in letter_types]
    ids = [file_name[:len(file_name) - 4] for file_name in os.listdir(source_path)]
    results = defaultdict(list)

    for letter_type in letter_types:
        for given_id in ids:
            route = route_template.format(letter_type, given_id)
            response = requests.get(route)
            if response.status_code == 200:
                print("success 200 with ({0},{1})".format(letter_type, given_id))
                results[letter_type].append(given_id)
                pdf = open(os.path.join(pdf_dir, letter_type, "{0}_for_mpi_id_{1}.pdf".format(letter_type, given_id)),
                           'wb')
                pdf.write(response.content)
                pdf.close()
            else:
                print("fail {0} with ({1},{2})".format(response.status_code, letter_type, given_id))

    print(results)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sourcePath = "C:/Users/622931/git_repos/lighthouse-mock-mpi/mock-mpi/src/main/resources/data/PRPA_IN201306UV02/profile_icn"
    hostName = "http://localhost"
    port = "8099"
    run_me(sourcePath, hostName, port)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
