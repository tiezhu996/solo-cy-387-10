import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { createBooking, delistProperty, getProperty, setFavorite } from '../api/client';
import { auth } from '../stores/auth';
const props = defineProps();
const router = useRouter();
const property = ref(null);
const error = ref('');
const notice = ref('');
const slots = ['周六 10:00', '周六 14:00', '周日 10:00', '周日 14:00'];
const slot = ref(slots[0]);
const favoritePending = ref(false);
const bookingPending = ref(false);
const delistPending = ref(false);
onMounted(async () => {
    try {
        property.value = await getProperty(Number(props.id));
    }
    catch (err) {
        error.value = err instanceof Error ? err.message : '房源加载失败';
    }
});
function requireLogin() {
    if (auth.token)
        return true;
    router.push({ name: 'login', query: { redirect: `/properties/${props.id}` } });
    return false;
}
async function toggleFavorite() {
    if (!property.value || favoritePending.value || !requireLogin())
        return;
    favoritePending.value = true;
    try {
        const state = await setFavorite(property.value.id, !property.value.favorited);
        property.value.favorited = state.favorited;
        property.value.favoriteCount = state.favoriteCount;
    }
    catch (err) {
        notice.value = err instanceof Error ? err.message : '操作失败';
    }
    finally {
        favoritePending.value = false;
    }
}
async function book() {
    if (!property.value || !property.value.bookable)
        return;
    bookingPending.value = true;
    notice.value = '';
    try {
        const booking = await createBooking(property.value.id, slot.value);
        notice.value = `预约成功：${booking.slot}，状态 ${booking.status}`;
    }
    catch (err) {
        notice.value = err instanceof Error ? err.message : '预约失败';
    }
    finally {
        bookingPending.value = false;
    }
}
async function delist() {
    if (!property.value)
        return;
    delistPending.value = true;
    try {
        property.value = await delistProperty(property.value.id);
        notice.value = '房源已下架，收藏夹中该房源已标记失效';
    }
    catch (err) {
        notice.value = err instanceof Error ? err.message : '下架失败';
    }
    finally {
        delistPending.value = false;
    }
}
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
__VLS_asFunctionalElement(__VLS_intrinsicElements.main, __VLS_intrinsicElements.main)({
    ...{ class: "page" },
});
const __VLS_0 = {}.ElButton;
/** @type {[typeof __VLS_components.ElButton, typeof __VLS_components.elButton, typeof __VLS_components.ElButton, typeof __VLS_components.elButton, ]} */ ;
// @ts-ignore
const __VLS_1 = __VLS_asFunctionalComponent(__VLS_0, new __VLS_0({
    ...{ 'onClick': {} },
    text: true,
}));
const __VLS_2 = __VLS_1({
    ...{ 'onClick': {} },
    text: true,
}, ...__VLS_functionalComponentArgsRest(__VLS_1));
let __VLS_4;
let __VLS_5;
let __VLS_6;
const __VLS_7 = {
    onClick: (...[$event]) => {
        __VLS_ctx.router.back();
    }
};
__VLS_3.slots.default;
var __VLS_3;
if (__VLS_ctx.error) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "error" },
    });
    (__VLS_ctx.error);
}
if (__VLS_ctx.property) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
        ...{ class: "detail" },
    });
    const __VLS_8 = {}.ElCarousel;
    /** @type {[typeof __VLS_components.ElCarousel, typeof __VLS_components.elCarousel, typeof __VLS_components.ElCarousel, typeof __VLS_components.elCarousel, ]} */ ;
    // @ts-ignore
    const __VLS_9 = __VLS_asFunctionalComponent(__VLS_8, new __VLS_8({
        ...{ class: "photos" },
        height: "320px",
    }));
    const __VLS_10 = __VLS_9({
        ...{ class: "photos" },
        height: "320px",
    }, ...__VLS_functionalComponentArgsRest(__VLS_9));
    __VLS_11.slots.default;
    for (const [photo, index] of __VLS_getVForSourceType((__VLS_ctx.property.photos))) {
        const __VLS_12 = {}.ElCarouselItem;
        /** @type {[typeof __VLS_components.ElCarouselItem, typeof __VLS_components.elCarouselItem, typeof __VLS_components.ElCarouselItem, typeof __VLS_components.elCarouselItem, ]} */ ;
        // @ts-ignore
        const __VLS_13 = __VLS_asFunctionalComponent(__VLS_12, new __VLS_12({
            key: (index),
        }));
        const __VLS_14 = __VLS_13({
            key: (index),
        }, ...__VLS_functionalComponentArgsRest(__VLS_13));
        __VLS_15.slots.default;
        __VLS_asFunctionalElement(__VLS_intrinsicElements.img)({
            src: (photo),
            alt: (`${__VLS_ctx.property.community} 照片 ${index + 1}`),
            ...{ class: "photo" },
        });
        var __VLS_15;
    }
    var __VLS_11;
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "detail-body" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "card-header" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({});
    (__VLS_ctx.property.community);
    const __VLS_16 = {}.ElTag;
    /** @type {[typeof __VLS_components.ElTag, typeof __VLS_components.elTag, typeof __VLS_components.ElTag, typeof __VLS_components.elTag, ]} */ ;
    // @ts-ignore
    const __VLS_17 = __VLS_asFunctionalComponent(__VLS_16, new __VLS_16({
        type: (__VLS_ctx.property.bookable ? 'success' : 'danger'),
    }));
    const __VLS_18 = __VLS_17({
        type: (__VLS_ctx.property.bookable ? 'success' : 'danger'),
    }, ...__VLS_functionalComponentArgsRest(__VLS_17));
    __VLS_19.slots.default;
    (__VLS_ctx.property.status);
    var __VLS_19;
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
    (__VLS_ctx.property.region);
    (__VLS_ctx.property.layout);
    (__VLS_ctx.property.area);
    (__VLS_ctx.property.payment);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "rent" },
    });
    (__VLS_ctx.property.rent);
    (__VLS_ctx.property.deposit);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.h3, __VLS_intrinsicElements.h3)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
    (__VLS_ctx.property.description);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.h3, __VLS_intrinsicElements.h3)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "facility-list" },
    });
    for (const [facility] of __VLS_getVForSourceType((__VLS_ctx.property.facilities))) {
        const __VLS_20 = {}.ElTag;
        /** @type {[typeof __VLS_components.ElTag, typeof __VLS_components.elTag, typeof __VLS_components.ElTag, typeof __VLS_components.elTag, ]} */ ;
        // @ts-ignore
        const __VLS_21 = __VLS_asFunctionalComponent(__VLS_20, new __VLS_20({
            key: (facility),
            size: "small",
        }));
        const __VLS_22 = __VLS_21({
            key: (facility),
            size: "small",
        }, ...__VLS_functionalComponentArgsRest(__VLS_21));
        __VLS_23.slots.default;
        (facility);
        var __VLS_23;
    }
    __VLS_asFunctionalElement(__VLS_intrinsicElements.h3, __VLS_intrinsicElements.h3)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
    (__VLS_ctx.property.landlordPhone);
    if (!__VLS_ctx.property.bookable) {
        const __VLS_24 = {}.ElAlert;
        /** @type {[typeof __VLS_components.ElAlert, typeof __VLS_components.elAlert, ]} */ ;
        // @ts-ignore
        const __VLS_25 = __VLS_asFunctionalComponent(__VLS_24, new __VLS_24({
            type: "error",
            closable: (false),
            title: "该房源已下架，无法预约看房",
        }));
        const __VLS_26 = __VLS_25({
            type: "error",
            closable: (false),
            title: "该房源已下架，无法预约看房",
        }, ...__VLS_functionalComponentArgsRest(__VLS_25));
    }
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "actions" },
    });
    const __VLS_28 = {}.ElButton;
    /** @type {[typeof __VLS_components.ElButton, typeof __VLS_components.elButton, typeof __VLS_components.ElButton, typeof __VLS_components.elButton, ]} */ ;
    // @ts-ignore
    const __VLS_29 = __VLS_asFunctionalComponent(__VLS_28, new __VLS_28({
        ...{ 'onClick': {} },
        type: (__VLS_ctx.property.favorited ? 'warning' : 'default'),
        loading: (__VLS_ctx.favoritePending),
    }));
    const __VLS_30 = __VLS_29({
        ...{ 'onClick': {} },
        type: (__VLS_ctx.property.favorited ? 'warning' : 'default'),
        loading: (__VLS_ctx.favoritePending),
    }, ...__VLS_functionalComponentArgsRest(__VLS_29));
    let __VLS_32;
    let __VLS_33;
    let __VLS_34;
    const __VLS_35 = {
        onClick: (__VLS_ctx.toggleFavorite)
    };
    __VLS_31.slots.default;
    (__VLS_ctx.property.favorited ? `★ 已收藏 (${__VLS_ctx.property.favoriteCount})` : `☆ 收藏 (${__VLS_ctx.property.favoriteCount})`);
    var __VLS_31;
    const __VLS_36 = {}.ElSelect;
    /** @type {[typeof __VLS_components.ElSelect, typeof __VLS_components.elSelect, typeof __VLS_components.ElSelect, typeof __VLS_components.elSelect, ]} */ ;
    // @ts-ignore
    const __VLS_37 = __VLS_asFunctionalComponent(__VLS_36, new __VLS_36({
        modelValue: (__VLS_ctx.slot),
        ...{ class: "slot-select" },
        disabled: (!__VLS_ctx.property.bookable),
    }));
    const __VLS_38 = __VLS_37({
        modelValue: (__VLS_ctx.slot),
        ...{ class: "slot-select" },
        disabled: (!__VLS_ctx.property.bookable),
    }, ...__VLS_functionalComponentArgsRest(__VLS_37));
    __VLS_39.slots.default;
    for (const [option] of __VLS_getVForSourceType((__VLS_ctx.slots))) {
        const __VLS_40 = {}.ElOption;
        /** @type {[typeof __VLS_components.ElOption, typeof __VLS_components.elOption, ]} */ ;
        // @ts-ignore
        const __VLS_41 = __VLS_asFunctionalComponent(__VLS_40, new __VLS_40({
            key: (option),
            label: (option),
            value: (option),
        }));
        const __VLS_42 = __VLS_41({
            key: (option),
            label: (option),
            value: (option),
        }, ...__VLS_functionalComponentArgsRest(__VLS_41));
    }
    var __VLS_39;
    const __VLS_44 = {}.ElButton;
    /** @type {[typeof __VLS_components.ElButton, typeof __VLS_components.elButton, typeof __VLS_components.ElButton, typeof __VLS_components.elButton, ]} */ ;
    // @ts-ignore
    const __VLS_45 = __VLS_asFunctionalComponent(__VLS_44, new __VLS_44({
        ...{ 'onClick': {} },
        type: "primary",
        disabled: (!__VLS_ctx.property.bookable),
        loading: (__VLS_ctx.bookingPending),
    }));
    const __VLS_46 = __VLS_45({
        ...{ 'onClick': {} },
        type: "primary",
        disabled: (!__VLS_ctx.property.bookable),
        loading: (__VLS_ctx.bookingPending),
    }, ...__VLS_functionalComponentArgsRest(__VLS_45));
    let __VLS_48;
    let __VLS_49;
    let __VLS_50;
    const __VLS_51 = {
        onClick: (__VLS_ctx.book)
    };
    __VLS_47.slots.default;
    var __VLS_47;
    if (__VLS_ctx.auth.user?.role === '房东' && __VLS_ctx.property.bookable) {
        const __VLS_52 = {}.ElButton;
        /** @type {[typeof __VLS_components.ElButton, typeof __VLS_components.elButton, typeof __VLS_components.ElButton, typeof __VLS_components.elButton, ]} */ ;
        // @ts-ignore
        const __VLS_53 = __VLS_asFunctionalComponent(__VLS_52, new __VLS_52({
            ...{ 'onClick': {} },
            type: "danger",
            plain: true,
            loading: (__VLS_ctx.delistPending),
        }));
        const __VLS_54 = __VLS_53({
            ...{ 'onClick': {} },
            type: "danger",
            plain: true,
            loading: (__VLS_ctx.delistPending),
        }, ...__VLS_functionalComponentArgsRest(__VLS_53));
        let __VLS_56;
        let __VLS_57;
        let __VLS_58;
        const __VLS_59 = {
            onClick: (__VLS_ctx.delist)
        };
        __VLS_55.slots.default;
        var __VLS_55;
    }
    if (__VLS_ctx.notice) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
            ...{ class: "notice" },
        });
        (__VLS_ctx.notice);
    }
}
/** @type {__VLS_StyleScopedClasses['page']} */ ;
/** @type {__VLS_StyleScopedClasses['error']} */ ;
/** @type {__VLS_StyleScopedClasses['detail']} */ ;
/** @type {__VLS_StyleScopedClasses['photos']} */ ;
/** @type {__VLS_StyleScopedClasses['photo']} */ ;
/** @type {__VLS_StyleScopedClasses['detail-body']} */ ;
/** @type {__VLS_StyleScopedClasses['card-header']} */ ;
/** @type {__VLS_StyleScopedClasses['rent']} */ ;
/** @type {__VLS_StyleScopedClasses['facility-list']} */ ;
/** @type {__VLS_StyleScopedClasses['actions']} */ ;
/** @type {__VLS_StyleScopedClasses['slot-select']} */ ;
/** @type {__VLS_StyleScopedClasses['notice']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            auth: auth,
            router: router,
            property: property,
            error: error,
            notice: notice,
            slots: slots,
            slot: slot,
            favoritePending: favoritePending,
            bookingPending: bookingPending,
            delistPending: delistPending,
            toggleFavorite: toggleFavorite,
            book: book,
            delist: delist,
        };
    },
    __typeProps: {},
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
    __typeProps: {},
});
; /* PartiallyEnd: #4569/main.vue */
