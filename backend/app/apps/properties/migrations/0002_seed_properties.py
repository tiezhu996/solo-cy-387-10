import urllib.parse

from django.db import migrations


def _photo(label: str, color: str) -> str:
    """生成离线可用的 SVG 占位图（data URI），避免依赖外部图床。"""
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='640' height='360'>"
        f"<rect width='100%' height='100%' fill='{color}'/>"
        f"<text x='50%' y='50%' fill='#ffffff' font-size='30' text-anchor='middle' "
        f"dominant-baseline='middle' font-family='sans-serif'>{label}</text></svg>"
    )
    return 'data:image/svg+xml;utf8,' + urllib.parse.quote(svg)


SAMPLE_PROPERTIES = [
    {
        'community': '海棠公寓', 'region': '滨江区', 'layout': '两室一厅', 'area': 76,
        'rent': 5200, 'deposit': 5200, 'payment': '月付',
        'facilities': ['空调', '洗衣机', '宽带'],
        'description': '朝南两室一厅，采光好，步行 5 分钟到地铁站，小区带电梯和门禁，适合上班族整租。',
        'photos': [_photo('海棠公寓 · 客厅', '#3a6ea5'), _photo('海棠公寓 · 主卧', '#5a8f7b'), _photo('海棠公寓 · 厨房', '#8f6f5a')],
        'status': '待出租', 'landlord_phone': '13800000001',
    },
    {
        'community': '梧桐里', 'region': '西湖区', 'layout': '一室一厅', 'area': 48,
        'rent': 3900, 'deposit': 3900, 'payment': '季付',
        'facilities': ['冰箱', '宽带'],
        'description': '精装一室一厅，家具家电齐全，拎包入住，周边商超和餐饮配套成熟。',
        'photos': [_photo('梧桐里 · 客厅', '#7a5a8f'), _photo('梧桐里 · 卧室', '#4a7a8f')],
        'status': '已预约', 'landlord_phone': '13800000002',
    },
    {
        'community': '江畔花园', 'region': '滨江区', 'layout': '三室两厅', 'area': 118,
        'rent': 8600, 'deposit': 8600, 'payment': '年付',
        'facilities': ['空调', '洗衣机', '冰箱', '宽带', '停车位'],
        'description': '江景大三房，双阳台，南北通透，适合家庭整租，可长租两年以上。',
        'photos': [_photo('江畔花园 · 客厅', '#2f6f4f'), _photo('江畔花园 · 阳台', '#6f4f2f'), _photo('江畔花园 · 主卧', '#4f2f6f')],
        'status': '待出租', 'landlord_phone': '13800000003',
    },
    {
        'community': '文汇里', 'region': '拱墅区', 'layout': '一室一厅', 'area': 42,
        'rent': 3100, 'deposit': 3100, 'payment': '月付',
        'facilities': ['空调', '宽带'],
        'description': '小户型一室一厅，近大学城，安静宜居，适合单人或情侣租住。',
        'photos': [_photo('文汇里 · 全景', '#8f3a3a'), _photo('文汇里 · 卧室', '#3a8f8f')],
        'status': '待出租', 'landlord_phone': '13800000004',
    },
]


def seed_properties(apps, schema_editor):
    Property = apps.get_model('properties', 'Property')
    for item in SAMPLE_PROPERTIES:
        Property.objects.get_or_create(community=item['community'], defaults=item)


def unseed_properties(apps, schema_editor):
    Property = apps.get_model('properties', 'Property')
    Property.objects.filter(community__in=[item['community'] for item in SAMPLE_PROPERTIES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_properties, unseed_properties),
    ]
