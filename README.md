<h1 align="center">PyBizfly Billing</h1>
<p align="center">Client hỗ trợ sử dụng API được cung cấp bởi BizFly Billing version 4th một cách đơn giản cho nội bộ Bizfly.</p>

## Cài đặt

Cài đặt sử dụng thông qua**pip**

    pip install pybizfly_billing

hoặc thông quan mã nguồn

    python setup.py install 

## Yêu cầu

- Thông tin cấu hình Openstack được sử dụng cho Billing v4.
- Id của khách hàng (tenant_id)

## Cấu hình

```python  
import pybilling

client = pybilling.BizFlyBillingClient()
```

<h2 id="tính-năng">Tính năng</h2>

PyBizfly hỗ trợ tất cả các tính năng được cung cấp
bởi [BizFly Cloud Cloud Server API](https://support.bizflycloud.vn/api/cloudserver/) cung cấp, bao gồm:

- [Truy vấn thông tin các kế hoạch sản phẩm](#plan)
- [Truy vấn thông tin, đăng ký và sử dụng tài nguyên](#subscription)

## Sử dụng

<h3 id="plan">Kế hoạch</h3>
PyBizfly Billing hỗ trợ truy vấn thông tin các kế hoạch sản phẩm.

[⬆ Quay lại Tính năng](#tính-năng)

Ví dụ này biểu diễn cách liệt kê các kế hoạch của của sản phẩm CPU cùng với các quan hệ liên quan.

```python
import pybilling

client = pybilling.BizFlyBillingClient()
plans = client.plan().list(embedded=['product', 'unit_prices'], filter_str='product.name=@CPU')

print(plans)
```

Ví dụ này biểu diễn cách lấy thông tin chi tiết của một kế hoạch.

```python
import pybilling

client = pybilling.BizFlyBillingClient()
cpu_plan = client.plan().get('07e17db4-6794-4af1-b33g-6fb78c2bf165', embedded=['product', 'unit_prices'])

print(cpu_plan)
```

<h3 id="subscription">Tài nguyên</h3>
PyBizfly hỗ trợ truy đăng ký, khai báo sử dụng và truy vấn thông tin tài nguyên theo khách hàng.

[⬆ Quay lại Tính năng](#tính-năng)

Ví dụ này biểu diễn đăng ký sử dụng tài nguyên sử dụng sản phẩm CPU 2 core premium trong 1 tháng.

```python
import pybilling

client = pybilling.BizFlyBillingClient()
subscription = client.subscription().create('cpu-1-month', resource_name='cpu-0001',
                                            resource_ref='07e17db4-6794-4af1-b33g-6fb78c2bf165',
                                            quantity=2, action='SUBSCRIBE', category_code='PR')

print(subscription)
```   

