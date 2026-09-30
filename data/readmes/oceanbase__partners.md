# OceanBase Community Partners

[中文版](README_CN.md)

OceanBase community ecological partners are part of the [OceanBase Partner Network](https://www.oceanbase.com/partner). According to the type of partners, they can be divided into solution partners and product ecological partners.

## Solution Partners

OceanBase community solution partners refer to ecological partners whose joint solutions with OceanBase CE have passed the compatibility certification. You can view the complete list of solution partners by visiting our website at https://www.oceanbase.com/partner/solution.

The certification process for OceanBase community solution partners is as follows:

1. Fill in the red part in [Test Report Template](solution/OceanBase数据库社区版&XXXX联合解决方案测试报告.docx).
2. Reply in [Who is using OceanBase](https://github.com/oceanbase/oceanbase/issues/1301) (Either Chinese or English is acceptable).
3. Contact the OceanBase team through the community’s [Contact Information](https://github.com/oceanbase/oceanbase?tab=readme-ov-file#community) and submit the test report.
4. After passing the review by the OceanBase team, we can go on the certificate electronic signature process.
5. After the signing workflow is completed, we will give you the certificate and update you to our web page.

## Product Ecological Partners

OceanBase community product ecological partners refer to the ecological partners of OceanBase Community Edition in the database business, which mainly include database tools, database middleware, and infrastructure such as chips and operating systems.

The files related to OceanBase community product ecological partners are stored in the current directory, mainly involving the following parts:

- `partners.yml`: The partners list in [Product Ecological Partner List](https://www.oceanbase.com/partner/product-ecology) page. If you want to update it, please directly create a pull request to modify this file.
- `landscape.yml`: The partners list displayed in [Product Ecological Partner Landscape](https://www.oceanbase.com/partner#ecology) page. If you want to update it, please make sure to add it to `partners.yml` firstly, then create an issue and attach the corresponding 400*128 pixel logo image for it.
- `logo`: The directory where logo images are stored. After your modification to landscape.yml is approved, OceanBase team members will update the image to this directory for you.

To add a new partner, you need provide the information as follows:

```yaml
  - id: Required, the partner id, it should consist of letters, numbers and dashes, and needs to be consistent with the partner’s name.
    name: Required, the partner name.
    logo: Optional, the logo path.
    website: Required, the official website of partner.
    description: Required, the description about partner.
    compatibility:
      - partner: Required, the name and version of partner product.
        ob: Required, the version of OceanBase.
        category: Required, the category of partner product.
        subcategory: Required, the category of partner product.
    references:
      - title: Required, reference link title.
        url: Required, reference link url.
```

## License

This repository is under the Apache License, Version 2.0, except for projects and products logos, which are generally copyrighted by the company or organization that created them, and are simply cached here for reliability. 
