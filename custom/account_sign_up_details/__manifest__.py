# -*- coding: utf-8 -*-

{
  "name"                 :  "Website Phone Number",
  "summary"              :  """Add a mandatory field for users to share their date of birth during the sign up.""",
  "category"             :  "Website",
  "version"              :  "15.0.2",
  "sequence"             :  1,
  "author"               :  "Usman Farzand",
  "license"              :  "Other proprietary",
  "website"              :  "https://odoospecialist.com",
  "description"          :  """https://odoospecialist.com""",
  "depends"              :  ['auth_signup'],
  "data"                 :  [
                             'views/res_partner_view.xml',
                             'views/account_details_template.xml',
                            ],
  # "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  # "pre_init_hook"        :  "pre_init_check",
}
