<script setup lang="tsx">
import { Form, FormSchema } from '@/components/Form'
import { useForm } from '@/hooks/web/useForm'
import { reactive, ref } from 'vue'
import { useValidator } from '@/hooks/web/useValidator'
import { useUserStoreWithOut } from '@/store/modules/user'
import { ElButton, ElMessage } from 'element-plus'
import { postCurrentUserUpdateInfo } from '@/api/admin/auth/user'

const { required, isTelephone } = useValidator()

const userStore = useUserStoreWithOut()

const formSchema = reactive<FormSchema[]>([
  {
    field: 'name',
    label: '用户名称',
    component: 'Input',
    colProps: {
      span: 24
    },
    formItemProps: {
      rules: [required()]
    },
    componentProps: {
      style: {
        width: '50%'
      }
    }
  },
  {
    field: 'nickname',
    label: '用户昵称',
    component: 'Input',
    colProps: {
      span: 24
    },
    componentProps: {
      style: {
        width: '50%'
      }
    }
  },
  {
    field: 'telephone',
    label: '手机号',
    component: 'Input',
    colProps: {
      span: 24
    },
    formItemProps: {
      rules: [required(), { validator: isTelephone, trigger: 'blur' }]
    },
    componentProps: {
      style: {
        width: '50%'
      },
      maxlength: 11
    }
  },
  {
    field: 'gender',
    label: '性别',
    colProps: {
      span: 24
    },
    formItemProps: {
      rules: [required()]
    },
    component: 'RadioGroup',
    componentProps: {
      options: [
        {
          label: '男',
          value: '0'
        },
        {
          label: '女',
          value: '1'
        }
      ]
    }
  },
  {
    field: 'save',
    colProps: {
      span: 24
    },
    formItemProps: {
      slots: {
        default: () => {
          return (
            <>
              <div class="w-[50%]">
                <ElButton loading={loading.value} type="primary" class="w-[100%]" onClick={save}>
                  保存
                </ElButton>
              </div>
            </>
          )
        }
      }
    }
  }
])

const { formRegister, formMethods } = useForm()
const { setValues, getFormData, getElFormExpose } = formMethods

setValues(userStore.getUser)
const loading = ref(false)

// 提交
const save = async () => {
  const elForm = await getElFormExpose()
  const valid = await elForm?.validate()
  if (valid) {
    loading.value = true
    const formData = await getFormData()
    try {
      const res = await postCurrentUserUpdateInfo(formData)
      if (res) {
        userStore.updateUser(res.data)
        ElMessage.success('保存成功')
      }
    } finally {
      loading.value = false
    }
  }
}
</script>

<template>
  <Form
    @register="formRegister"
    :schema="formSchema"
    hide-required-asterisk
    class="dark:(border-1 border-[var(--el-border-color)] border-solid)"
  />
</template>
