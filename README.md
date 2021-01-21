<h1 align="center">PyBizfly Billing</h1>
<p align="center">Client hỗ trợ sử dụng API được cung cấp bởi BizFly Billing version 4th một cách đơn giản cho nội bộ Bizfly.</p>

## Cài đặt

Cài đặt sử dụng thông qua**pip**

    pip install git+https://github.com/milkandpie/pybizfly-billing.git

hoặc thông quan mã nguồn
    
    git clone https://github.com/milkandpie/pybizfly-billing.git
    cd pybizfly-billing   
    python setup.py install 

## Yêu cầu

- Thông tin cấu hình Openstack được sử dụng cho Billing v4.
- Id của khách hàng (tenant_id).
- API url của Billing v4.

## Cấu hình
Các giá trị trong `config` có thể lấy từ môi trường hoặc trực tiếp truyền vào khi khởi tạo client.

Giá trị `api_url` là url api Billing v4. Có thể đặt biến môi trường với khóa là `BILLING_API_URL`. Nếu không, giá trị mặc định là [BILLING API V4](https://billing.bizflycloud.vn/api/v4/)

```python  
import pybilling

client = pybilling.BizFlyBillingClient(
    tenant_id='5a72fb63165b4d3fada838da329b94a3',
    api_url='https://dev-billing.bizflycloud.vn',
    config={
        "OPENSTACK_AUTH_URL": "",
        "KEYSTONE_TENANT_ADMIN": "",
        "OPENSTACK_DEFAULT_PROJECT_DOMAIN_NAME": "",
        "KEYSTONE_AUTH_PLUGIN": "",
        "KEYSTONE_USER_ADMIN": "",
        "KEYSTONE_PASSWORD_ADMIN": "",
        "OPENSTACK_DEFAULT_USER_DOMAIN_NAME": "",
    }
)
```

hoặc

```python  
import pybilling

client = pybilling.BizFlyBillingClient(
    tenant_id='5a72fb63165b4d3fada838da329b94a3',
    api_url='https://dev-billing.bizflycloud.vn'
    access_token='gAAAAABf9X2QuVi1tRJAoCt8jypeKRMlQ96q5sZJgW66XtAlkcbw8aAySJVLzcPHBqZEE8S1RrgYIMf5GsjJ38Tu8gaGiz_35vbyTOfLEDdsJxLBVcmWoVQJ6GkZ8aaYNz098SL5-6ar1xStpQqxIKPoJ9UOb2_T0m5g8HnN0gxzfKmTP9vzIWk'
)
```

<h2 id="tính-năng">Tính năng</h2>

PyBizfly hỗ trợ tất cả các tính năng được cung cấp
bởi [BizFly Cloud Cloud Server API](https://support.bizflycloud.vn/api/cloudserver/) cung cấp, bao gồm:

- [Truy vấn thông tin các kế hoạch sản phẩm](#plan)
- [Truy vấn thông tin, đăng ký và sử dụng tài nguyên](#subscription)
- [Truy vấn thông tin tài khoản](#account)

## Sử dụng

<h3 id="plan">Kế hoạch</h3>
PyBizfly Billing hỗ trợ truy vấn thông tin các kế hoạch sản phẩm.

[⬆ Quay lại Tính năng](#tính-năng)

Ví dụ này biểu diễn cách liệt kê các kế hoạch của của sản phẩm CPU cùng với các quan hệ liên quan.
Tạo client với lựa chọn with_access_token là False cho các request không cần xác thực.
```python
import pybilling

client = pybilling.BizFlyBillingClient(with_access_token=False)
plans = client.plan().list(embedded=['product', 'unit_prices'], filter_str='product.name=@CPU')

print(plans)
```

Ví dụ này biểu diễn cách lấy thông tin chi tiết của một kế hoạch.

```python
import pybilling

client = pybilling.BizFlyBillingClient(with_access_token=False)
cpu_plan = client.plan().get('07e17db4-6794-4af1-b33g-6fb78c2bf165', embedded=['product', 'unit_prices'])

print(cpu_plan)
```

<h3 id="subscription">Tài nguyên</h3>
PyBizfly hỗ trợ truy đăng ký, khai báo sử dụng và truy vấn thông tin tài nguyên theo khách hàng.

[⬆ Quay lại Tính năng](#tính-năng)

Ví dụ này biểu diễn đăng ký sử dụng tài nguyên sử dụng sản phẩm Machine 20 GB trong 1 tháng.

```python
import pybilling

client = pybilling.BizFlyBillingClient(
    tenant_id='5a72fb63165b4d3fada838da329b94a3',
    api_url='https://dev-billing.bizflycloud.vn',
    access_token='gAAAAABf9X2QuVi1tRJAoCt8jypeKRMlQ96q5sZJgW66XtAlkcbw8aAySJVLzcPHBqZEE8S1RrgYIMf5GsjJ38Tu8gaGiz_35vbyTOfLEDdsJxLBVcmWoVQJ6GkZ8aaYNz098SL5-6ar1xStpQqxIKPoJ9UOb2_T0m5g8HnN0gxzfKmTP9vzIWk'
)

subscription_service = client.subscription()
print(subscription_service.subscribe('machine_a_month', 'machine_01', '07e17db4-6794-4af1-b33g-6fb78c2bf165'))
```   

Ví dụ này biểu diễn cập nhật sử dụng tài nguyên sử dụng sản phẩm Data Tranfer 20 GB trong tháng.

```python
import pybilling

client = pybilling.BizFlyBillingClient(
    tenant_id='5a72fb63165b4d3fada838da329b94a3',
    api_url='https://dev-billing.bizflycloud.vn',
    access_token='gAAAAABf9X2QuVi1tRJAoCt8jypeKRMlQ96q5sZJgW66XtAlkcbw8aAySJVLzcPHBqZEE8S1RrgYIMf5GsjJ38Tu8gaGiz_35vbyTOfLEDdsJxLBVcmWoVQJ6GkZ8aaYNz098SL5-6ar1xStpQqxIKPoJ9UOb2_T0m5g8HnN0gxzfKmTP9vzIWk'
)

subscription_service = client.subscription()
print(subscription_service.log('data_transfer', 'machine_01', '07e17db4-6794-4af1-b33g-6fb78c2bf165', 100))
```   

Ví dụ này biểu diễn kết thúc sử dụng tài nguyên sử dụng sản phẩm Data Tranfer 20 GB trong tháng.
```python
import pybilling

client = pybilling.BizFlyBillingClient(
    tenant_id='5a72fb63165b4d3fada838da329b94a3',
    api_url='https://dev-billing.bizflycloud.vn',
    access_token='gAAAAABf9X2QuVi1tRJAoCt8jypeKRMlQ96q5sZJgW66XtAlkcbw8aAySJVLzcPHBqZEE8S1RrgYIMf5GsjJ38Tu8gaGiz_35vbyTOfLEDdsJxLBVcmWoVQJ6GkZ8aaYNz098SL5-6ar1xStpQqxIKPoJ9UOb2_T0m5g8HnN0gxzfKmTP9vzIWk'
)

subscription_service = client.subscription()
print(subscription_service.close('data_transfer', 'machine_01', '07e17db4-6794-4af1-b33g-6fb78c2bf165'))
```  

Ví dụ dưới đây biểu diễn truy vấn sử dụng tài nguyên sử dụng sản phẩm Machine của tài khoản cùng với chi tiết sử dụng.
```python
import pybilling

client = pybilling.BizFlyBillingClient(
    tenant_id='5a72fb63165b4d3fada838da329b94a3',
    api_url='https://dev-billing.bizflycloud.vn',
    access_token='gAAAAABf9X2QuVi1tRJAoCt8jypeKRMlQ96q5sZJgW66XtAlkcbw8aAySJVLzcPHBqZEE8S1RrgYIMf5GsjJ38Tu8gaGiz_35vbyTOfLEDdsJxLBVcmWoVQJ6GkZ8aaYNz098SL5-6ar1xStpQqxIKPoJ9UOb2_T0m5g8HnN0gxzfKmTP9vzIWk'
)

subscription_service = client.subscription()
print(subscription_service.get('2bfe6e25-2a69-40ba-abd9-fa364cbecc7f', embedded=['usages']))
```   

```python
import pybilling

client = pybilling.BizFlyBillingClient(
    tenant_id='5a72fb63165b4d3fada838da329b94a3',
    api_url='https://dev-billing.bizflycloud.vn',
    access_token='gAAAAABf9X2QuVi1tRJAoCt8jypeKRMlQ96q5sZJgW66XtAlkcbw8aAySJVLzcPHBqZEE8S1RrgYIMf5GsjJ38Tu8gaGiz_35vbyTOfLEDdsJxLBVcmWoVQJ6GkZ8aaYNz098SL5-6ar1xStpQqxIKPoJ9UOb2_T0m5g8HnN0gxzfKmTP9vzIWk'
)

subscription_service = client.subscription()
print(subscription_service.list(embedded=['usages'], filter_str='plan.summary==machine_a_month'))
```


Ví dụ dưới đây biểu diễn cách đổi kế hoạch sản phẩm Data transfer sang dùng thử.
```python
import pybilling

client = pybilling.BizFlyBillingClient(
    tenant_id='5a72fb63165b4d3fada838da329b94a3',
    api_url='https://dev-billing.bizflycloud.vn',
    access_token='gAAAAABf9X2QuVi1tRJAoCt8jypeKRMlQ96q5sZJgW66XtAlkcbw8aAySJVLzcPHBqZEE8S1RrgYIMf5GsjJ38Tu8gaGiz_35vbyTOfLEDdsJxLBVcmWoVQJ6GkZ8aaYNz098SL5-6ar1xStpQqxIKPoJ9UOb2_T0m5g8HnN0gxzfKmTP9vzIWk'
)

subscription_service = client.subscription()
print(subscription_service.switch_plan('data_transfer', 'data_tf_01', '2bfe6e25-2a69-40ba-abd9-fa364cbecc7f',
                                       switchable_plan_name='data_transfer_trial'))
``` 

Ví dụ dưới đây biểu diễn cách đổi kế hoạch sản phẩm Data transfer từ dùng thử lên trả phí. 
```python
import pybilling

client = pybilling.BizFlyBillingClient(
    tenant_id='5a72fb63165b4d3fada838da329b94a3',
    api_url='https://dev-billing.bizflycloud.vn',
    access_token='gAAAAABf9X2QuVi1tRJAoCt8jypeKRMlQ96q5sZJgW66XtAlkcbw8aAySJVLzcPHBqZEE8S1RrgYIMf5GsjJ38Tu8gaGiz_35vbyTOfLEDdsJxLBVcmWoVQJ6GkZ8aaYNz098SL5-6ar1xStpQqxIKPoJ9UOb2_T0m5g8HnN0gxzfKmTP9vzIWk'
)

subscription_service = client.subscription()
print(subscription_service.upgrade_trial('data_transfer_trial', 'data_tf_01', '2bfe6e25-2a69-40ba-abd9-fa364cbecc7f'))
``` 

<h3 id="account">Tài khoản</h3>
PyBizfly Billing hỗ trợ truy vấn thông tin tài khoản thông qua token admin.

[⬆ Quay lại Tính năng](#tính-năng)

Ví dụ này biểu diễn cách liệt kê danh sách 25 tài khoản theo thời gian tạo với thứ tự đảo ngược.
```python
import pybilling

client = pybilling.BizFlyBillingClient(
    tenant_id='5a72fb63165b4d3fada838da329b94a3',
    api_url='https://dev-billing.bizflycloud.vn',
    access_token='gAAAAABf9X2QuVi1tRJAoCt8jypeKRMlQ96q5sZJgW66XtAlkcbw8aAySJVLzcPHBqZEE8S1RrgYIMf5GsjJ38Tu8gaGiz_35vbyTOfLEDdsJxLBVcmWoVQJ6GkZ8aaYNz098SL5-6ar1xStpQqxIKPoJ9UOb2_T0m5g8HnN0gxzfKmTP9vzIWk'
)
accounts = client.account().list(sort='_created', ascending=False, limit=25)

print(accounts)
```