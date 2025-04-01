from login_dp import main
from sc_login_aeskey_api import run_admin_login_workflow
from sc_dp_risk import DepositRiskProcessor

main()
run_admin_login_workflow()
processor = DepositRiskProcessor()
processor.run()