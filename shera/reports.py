import os
import csv
import base64
import topdf
import tempfile
import shutil


def get_reports(contracts_path, reports_path):
    def is_valid(x):
        return x is not None and x not in ['', '""']

    def is_valid_file(reports_path, x):
        return os.path.exists(os.path.join(reports_path, x))

    reports = []
    with open(contracts_path, 'rb') as file_:
        reader = csv.reader(file_, delimiter=';', quotechar='|')
        reports = [{
            'contract_id': contract[0],
            'CUPS': contract[1],
            'report': os.path.join(reports_path, contract[-1]),
            'report_name': contract[-1]
        } for contract in reader if (
            contract and
            is_valid(contract[0]) and
            is_valid_file(reports_path, contract[-1])
        )]
    return reports


def render_reports(O, reports, template_name, output):
    path_aux = tempfile.mkdtemp()
    failed = []
    for report_idx, report in enumerate(reports):
        partner_data = None
        try:
            partner_data = O.get_partner_data(report['CUPS'])
        except Exception:
            partner_data = None
        if not partner_data:
            failed.append(report_idx)
            continue
        report.update(partner_data)
        try:
            new_report = topdf.customize(
                report=report,
                template_name=template_name,
                path_aux=path_aux,
                path_output=output
            )
            reports[report_idx]['pdf'] = None
            with open(new_report, 'rb') as report_file:
                data = base64.b64encode(report_file.read())
                reports[report_idx]['pdf'] = data
            if not reports[report_idx]['pdf']:
                raise Exception('Null report pdf content')
        except Exception:
            failed.append(report_idx)
    for idx in failed:
        del reports[idx]
    shutil.rmtree(path_aux)
