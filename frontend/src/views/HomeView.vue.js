import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import PropertyCard from '../components/PropertyCard.vue';
import { createBooking, createRepair, getProperties, setFavorite } from '../api/client';
import { auth } from '../stores/auth';
const router = useRouter();
const properties = ref([]);
const mode = ref('列表视图');
const region = ref('');
const maxRent = ref(7000);
const layout = ref('全部');
const faultType = ref('水电');
const description = ref('');
const repairNotice = ref('等待提交');
const notice = ref('');
const loadError = ref('');
const favoritePendingId = ref(null);
onMounted(async () => {
    try {
        properties.value = await getProperties();
    }
    catch {
        loadError.value = '房源加载失败，请稍后重试';
    }
});
const filtered = computed(() => properties.value.filter((item) => {
    const hitRegion = !region.value || item.region.includes(region.value);
    const hitRent = item.rent <= maxRent.value;
    const hitLayout = layout.value === '全部' || item.layout === layout.value;
    return hitRegion && hitRent && hitLayout;
}));
function requireLogin() {
    if (auth.token)
        return true;
    router.push({ name: 'login', query: { redirect: '/' } });
    return false;
}
async function toggleFavorite(item) {
    if (favoritePendingId.value !== null || !requireLogin())
        return;
    favoritePendingId.value = item.id;
    try {
        const state = await setFavorite(item.id, !item.favorited);
        item.favorited = state.favorited;
        item.favoriteCount = state.favoriteCount;
    }
    catch (err) {
        notice.value = err instanceof Error ? err.message : '收藏操作失败';
    }
    finally {
        favoritePendingId.value = null;
    }
}
async function book(item) {
    if (!item.bookable)
        return;
    try {
        const booking = await createBooking(item.id, '周六 10:00');
        notice.value = `预约成功：${item.community} ${booking.slot}，状态 ${booking.status}`;
    }
    catch (err) {
        notice.value = err instanceof Error ? err.message : '预约失败';
    }
}
async function submitRepair() {
    const ticket = await createRepair({ faultType: faultType.value, description: description.value });
    repairNotice.value = `工单 ${ticket.id} 已提交：${ticket.status}`;
}
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.main, __VLS_intrinsicElements.main)({
    ...{ class: "page" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "toolbar" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
const __VLS_0 = {}.ElSegmented;
/** @type {[typeof __VLS_components.ElSegmented, typeof __VLS_components.elSegmented, ]} */ ;
// @ts-ignore
const __VLS_1 = __VLS_asFunctionalComponent(__VLS_0, new __VLS_0({
    modelValue: (__VLS_ctx.mode),
    options: (['列表视图', '地图视图']),
}));
const __VLS_2 = __VLS_1({
    modelValue: (__VLS_ctx.mode),
    options: (['列表视图', '地图视图']),
}, ...__VLS_functionalComponentArgsRest(__VLS_1));
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "filters" },
});
const __VLS_4 = {}.ElInput;
/** @type {[typeof __VLS_components.ElInput, typeof __VLS_components.elInput, ]} */ ;
// @ts-ignore
const __VLS_5 = __VLS_asFunctionalComponent(__VLS_4, new __VLS_4({
    modelValue: (__VLS_ctx.region),
    placeholder: "区域",
}));
const __VLS_6 = __VLS_5({
    modelValue: (__VLS_ctx.region),
    placeholder: "区域",
}, ...__VLS_functionalComponentArgsRest(__VLS_5));
const __VLS_8 = {}.ElInputNumber;
/** @type {[typeof __VLS_components.ElInputNumber, typeof __VLS_components.elInputNumber, ]} */ ;
// @ts-ignore
const __VLS_9 = __VLS_asFunctionalComponent(__VLS_8, new __VLS_8({
    modelValue: (__VLS_ctx.maxRent),
    min: (1000),
    step: (500),
}));
const __VLS_10 = __VLS_9({
    modelValue: (__VLS_ctx.maxRent),
    min: (1000),
    step: (500),
}, ...__VLS_functionalComponentArgsRest(__VLS_9));
const __VLS_12 = {}.ElSelect;
/** @type {[typeof __VLS_components.ElSelect, typeof __VLS_components.elSelect, typeof __VLS_components.ElSelect, typeof __VLS_components.elSelect, ]} */ ;
// @ts-ignore
const __VLS_13 = __VLS_asFunctionalComponent(__VLS_12, new __VLS_12({
    modelValue: (__VLS_ctx.layout),
    placeholder: "户型",
}));
const __VLS_14 = __VLS_13({
    modelValue: (__VLS_ctx.layout),
    placeholder: "户型",
}, ...__VLS_functionalComponentArgsRest(__VLS_13));
__VLS_15.slots.default;
const __VLS_16 = {}.ElOption;
/** @type {[typeof __VLS_components.ElOption, typeof __VLS_components.elOption, ]} */ ;
// @ts-ignore
const __VLS_17 = __VLS_asFunctionalComponent(__VLS_16, new __VLS_16({
    label: "全部",
    value: "全部",
}));
const __VLS_18 = __VLS_17({
    label: "全部",
    value: "全部",
}, ...__VLS_functionalComponentArgsRest(__VLS_17));
const __VLS_20 = {}.ElOption;
/** @type {[typeof __VLS_components.ElOption, typeof __VLS_components.elOption, ]} */ ;
// @ts-ignore
const __VLS_21 = __VLS_asFunctionalComponent(__VLS_20, new __VLS_20({
    label: "一室一厅",
    value: "一室一厅",
}));
const __VLS_22 = __VLS_21({
    label: "一室一厅",
    value: "一室一厅",
}, ...__VLS_functionalComponentArgsRest(__VLS_21));
const __VLS_24 = {}.ElOption;
/** @type {[typeof __VLS_components.ElOption, typeof __VLS_components.elOption, ]} */ ;
// @ts-ignore
const __VLS_25 = __VLS_asFunctionalComponent(__VLS_24, new __VLS_24({
    label: "两室一厅",
    value: "两室一厅",
}));
const __VLS_26 = __VLS_25({
    label: "两室一厅",
    value: "两室一厅",
}, ...__VLS_functionalComponentArgsRest(__VLS_25));
const __VLS_28 = {}.ElOption;
/** @type {[typeof __VLS_components.ElOption, typeof __VLS_components.elOption, ]} */ ;
// @ts-ignore
const __VLS_29 = __VLS_asFunctionalComponent(__VLS_28, new __VLS_28({
    label: "三室两厅",
    value: "三室两厅",
}));
const __VLS_30 = __VLS_29({
    label: "三室两厅",
    value: "三室两厅",
}, ...__VLS_functionalComponentArgsRest(__VLS_29));
var __VLS_15;
if (__VLS_ctx.mode === '地图视图') {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
        ...{ class: "map-panel" },
    });
    (__VLS_ctx.filtered.length);
}
if (__VLS_ctx.loadError) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "error" },
    });
    (__VLS_ctx.loadError);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "grid" },
});
for (const [item] of __VLS_getVForSourceType((__VLS_ctx.filtered))) {
    /** @type {[typeof PropertyCard, ]} */ ;
    // @ts-ignore
    const __VLS_32 = __VLS_asFunctionalComponent(PropertyCard, new PropertyCard({
        ...{ 'onView': {} },
        ...{ 'onToggleFavorite': {} },
        ...{ 'onBook': {} },
        key: (item.id),
        item: (item),
        favoritePending: (__VLS_ctx.favoritePendingId === item.id),
    }));
    const __VLS_33 = __VLS_32({
        ...{ 'onView': {} },
        ...{ 'onToggleFavorite': {} },
        ...{ 'onBook': {} },
        key: (item.id),
        item: (item),
        favoritePending: (__VLS_ctx.favoritePendingId === item.id),
    }, ...__VLS_functionalComponentArgsRest(__VLS_32));
    let __VLS_35;
    let __VLS_36;
    let __VLS_37;
    const __VLS_38 = {
        onView: ((id) => __VLS_ctx.router.push(`/properties/${id}`))
    };
    const __VLS_39 = {
        onToggleFavorite: (__VLS_ctx.toggleFavorite)
    };
    const __VLS_40 = {
        onBook: (__VLS_ctx.book)
    };
    var __VLS_34;
}
if (__VLS_ctx.notice) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "notice" },
    });
    (__VLS_ctx.notice);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "repair" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
const __VLS_41 = {}.ElSelect;
/** @type {[typeof __VLS_components.ElSelect, typeof __VLS_components.elSelect, typeof __VLS_components.ElSelect, typeof __VLS_components.elSelect, ]} */ ;
// @ts-ignore
const __VLS_42 = __VLS_asFunctionalComponent(__VLS_41, new __VLS_41({
    modelValue: (__VLS_ctx.faultType),
}));
const __VLS_43 = __VLS_42({
    modelValue: (__VLS_ctx.faultType),
}, ...__VLS_functionalComponentArgsRest(__VLS_42));
__VLS_44.slots.default;
const __VLS_45 = {}.ElOption;
/** @type {[typeof __VLS_components.ElOption, typeof __VLS_components.elOption, ]} */ ;
// @ts-ignore
const __VLS_46 = __VLS_asFunctionalComponent(__VLS_45, new __VLS_45({
    label: "水电",
    value: "水电",
}));
const __VLS_47 = __VLS_46({
    label: "水电",
    value: "水电",
}, ...__VLS_functionalComponentArgsRest(__VLS_46));
const __VLS_49 = {}.ElOption;
/** @type {[typeof __VLS_components.ElOption, typeof __VLS_components.elOption, ]} */ ;
// @ts-ignore
const __VLS_50 = __VLS_asFunctionalComponent(__VLS_49, new __VLS_49({
    label: "门锁",
    value: "门锁",
}));
const __VLS_51 = __VLS_50({
    label: "门锁",
    value: "门锁",
}, ...__VLS_functionalComponentArgsRest(__VLS_50));
const __VLS_53 = {}.ElOption;
/** @type {[typeof __VLS_components.ElOption, typeof __VLS_components.elOption, ]} */ ;
// @ts-ignore
const __VLS_54 = __VLS_asFunctionalComponent(__VLS_53, new __VLS_53({
    label: "管道",
    value: "管道",
}));
const __VLS_55 = __VLS_54({
    label: "管道",
    value: "管道",
}, ...__VLS_functionalComponentArgsRest(__VLS_54));
const __VLS_57 = {}.ElOption;
/** @type {[typeof __VLS_components.ElOption, typeof __VLS_components.elOption, ]} */ ;
// @ts-ignore
const __VLS_58 = __VLS_asFunctionalComponent(__VLS_57, new __VLS_57({
    label: "家电",
    value: "家电",
}));
const __VLS_59 = __VLS_58({
    label: "家电",
    value: "家电",
}, ...__VLS_functionalComponentArgsRest(__VLS_58));
const __VLS_61 = {}.ElOption;
/** @type {[typeof __VLS_components.ElOption, typeof __VLS_components.elOption, ]} */ ;
// @ts-ignore
const __VLS_62 = __VLS_asFunctionalComponent(__VLS_61, new __VLS_61({
    label: "其他",
    value: "其他",
}));
const __VLS_63 = __VLS_62({
    label: "其他",
    value: "其他",
}, ...__VLS_functionalComponentArgsRest(__VLS_62));
var __VLS_44;
const __VLS_65 = {}.ElInput;
/** @type {[typeof __VLS_components.ElInput, typeof __VLS_components.elInput, ]} */ ;
// @ts-ignore
const __VLS_66 = __VLS_asFunctionalComponent(__VLS_65, new __VLS_65({
    modelValue: (__VLS_ctx.description),
    placeholder: "描述故障情况",
}));
const __VLS_67 = __VLS_66({
    modelValue: (__VLS_ctx.description),
    placeholder: "描述故障情况",
}, ...__VLS_functionalComponentArgsRest(__VLS_66));
const __VLS_69 = {}.ElButton;
/** @type {[typeof __VLS_components.ElButton, typeof __VLS_components.elButton, typeof __VLS_components.ElButton, typeof __VLS_components.elButton, ]} */ ;
// @ts-ignore
const __VLS_70 = __VLS_asFunctionalComponent(__VLS_69, new __VLS_69({
    ...{ 'onClick': {} },
    type: "success",
}));
const __VLS_71 = __VLS_70({
    ...{ 'onClick': {} },
    type: "success",
}, ...__VLS_functionalComponentArgsRest(__VLS_70));
let __VLS_73;
let __VLS_74;
let __VLS_75;
const __VLS_76 = {
    onClick: (__VLS_ctx.submitRepair)
};
__VLS_72.slots.default;
var __VLS_72;
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
(__VLS_ctx.repairNotice);
/** @type {__VLS_StyleScopedClasses['page']} */ ;
/** @type {__VLS_StyleScopedClasses['toolbar']} */ ;
/** @type {__VLS_StyleScopedClasses['filters']} */ ;
/** @type {__VLS_StyleScopedClasses['map-panel']} */ ;
/** @type {__VLS_StyleScopedClasses['error']} */ ;
/** @type {__VLS_StyleScopedClasses['grid']} */ ;
/** @type {__VLS_StyleScopedClasses['notice']} */ ;
/** @type {__VLS_StyleScopedClasses['repair']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            PropertyCard: PropertyCard,
            router: router,
            mode: mode,
            region: region,
            maxRent: maxRent,
            layout: layout,
            faultType: faultType,
            description: description,
            repairNotice: repairNotice,
            notice: notice,
            loadError: loadError,
            favoritePendingId: favoritePendingId,
            filtered: filtered,
            toggleFavorite: toggleFavorite,
            book: book,
            submitRepair: submitRepair,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
