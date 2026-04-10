<script lang="ts">
  import PageLayout from '$lib/components/PageLayout.svelte';
  import { User, Mail, Coffee, Settings, Bell, Eye, Lock, HelpCircle, LogOut, ChevronRight, Thermometer, Scale } from 'lucide-svelte';
  import { getSettings, updateSettings } from '$lib/settings.svelte';
  import type { TempUnit, WeightUnit } from '$lib/settings.svelte';

  let settings = $derived(getSettings());

  function setTempUnit(unit: TempUnit) { updateSettings({ tempUnit: unit }); }
  function setWeightUnit(unit: WeightUnit) { updateSettings({ weightUnit: unit }); }
  function setGrinder(e: Event) { updateSettings({ grinder: (e.target as HTMLSelectElement).value }); }
  function toggleNotifications() { updateSettings({ notifications: !settings.notifications }); }
  function togglePublicProfile() { updateSettings({ publicProfile: !settings.publicProfile }); }
</script>

<PageLayout title="Profile">
  <div class="space-y-6">
    <!-- User Profile -->
    <div class="p-6 bg-white border border-neutral-200 rounded-lg">
      <div class="flex items-start gap-4">
        <div class="w-16 h-16 bg-gradient-to-br from-amber-400 to-amber-600 rounded-full flex items-center justify-center flex-shrink-0">
          <User class="w-8 h-8 text-white" />
        </div>
        <div class="flex-1">
          <h3 class="font-semibold text-amber-900">Coffee Enthusiast</h3>
          <p class="text-sm text-neutral-600">coffeelov3r@email.com</p>
          <button class="mt-3 border border-neutral-300 text-neutral-700 text-sm py-1.5 px-3 rounded-lg hover:bg-neutral-50 transition-colors">
            Edit Profile
          </button>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="p-6 bg-white border border-neutral-200 rounded-lg">
      <h3 class="font-semibold text-amber-900 mb-4">Your Stats</h3>
      <div class="grid grid-cols-3 gap-4">
        {#each [[24, 'Brews'], [8, 'Recipes'], ['4.2', 'Avg Rating']] as [val, label]}
          <div class="text-center">
            <div class="text-2xl font-semibold text-amber-900">{val}</div>
            <div class="text-xs text-neutral-600">{label}</div>
          </div>
        {/each}
      </div>
    </div>

    <!-- Grinder Settings -->
    <div class="p-6 bg-white border border-neutral-200 rounded-lg">
      <div class="flex items-center gap-2 mb-4">
        <Coffee class="w-5 h-5 text-amber-700" />
        <h3 class="font-semibold text-amber-900">Grinder Settings</h3>
      </div>
      <div class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-neutral-700 mb-1.5" for="grinder">Your Grinder</label>
          <select id="grinder" value={settings.grinder} onchange={setGrinder} class="w-full border border-neutral-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white">
            <option value="fellow-ode">Fellow Ode</option>
            <option value="fellow-ode-gen2">Fellow Ode Gen 2</option>
            <option value="baratza-encore">Baratza Encore</option>
            <option value="baratza-virtuoso">Baratza Virtuoso+</option>
            <option value="comandante">Comandante C40</option>
            <option value="1zpresso">1Zpresso JX-Pro</option>
            <option value="other">Other</option>
          </select>
        </div>

        <!-- Temperature Unit -->
        <div>
          <label class="flex items-center gap-1.5 text-sm font-medium text-neutral-700 mb-1.5">
            <Thermometer class="w-3.5 h-3.5" /> Temperature
          </label>
          <div class="grid grid-cols-2 bg-neutral-100 rounded-lg p-1 gap-1">
            <button
              onclick={() => setTempUnit('C')}
              class="py-2 text-sm rounded-md transition-all {settings.tempUnit === 'C' ? 'bg-white text-amber-900 shadow-sm font-medium' : 'text-neutral-600 hover:text-neutral-800'}"
            >°C — Celsius</button>
            <button
              onclick={() => setTempUnit('F')}
              class="py-2 text-sm rounded-md transition-all {settings.tempUnit === 'F' ? 'bg-white text-amber-900 shadow-sm font-medium' : 'text-neutral-600 hover:text-neutral-800'}"
            >°F — Fahrenheit</button>
          </div>
        </div>

        <!-- Weight Unit -->
        <div>
          <label class="flex items-center gap-1.5 text-sm font-medium text-neutral-700 mb-1.5">
            <Scale class="w-3.5 h-3.5" /> Weight
          </label>
          <div class="grid grid-cols-2 bg-neutral-100 rounded-lg p-1 gap-1">
            <button
              onclick={() => setWeightUnit('g')}
              class="py-2 text-sm rounded-md transition-all {settings.weightUnit === 'g' ? 'bg-white text-amber-900 shadow-sm font-medium' : 'text-neutral-600 hover:text-neutral-800'}"
            >g — Grams</button>
            <button
              onclick={() => setWeightUnit('mL')}
              class="py-2 text-sm rounded-md transition-all {settings.weightUnit === 'mL' ? 'bg-white text-amber-900 shadow-sm font-medium' : 'text-neutral-600 hover:text-neutral-800'}"
            >mL — Milliliters</button>
          </div>
          <p class="text-xs text-neutral-400 mt-1.5">Particle sizes are always shown in μm</p>
        </div>
      </div>
    </div>

    <!-- Preferences -->
    <div class="p-6 bg-white border border-neutral-200 rounded-lg">
      <div class="flex items-center gap-2 mb-4">
        <Settings class="w-5 h-5 text-amber-700" />
        <h3 class="font-semibold text-amber-900">Preferences</h3>
      </div>
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <Bell class="w-4 h-4 text-neutral-500" />
            <div>
              <div class="text-sm font-medium text-neutral-700">Notifications</div>
              <div class="text-xs text-neutral-500">Get brew reminders and tips</div>
            </div>
          </div>
          <button
            onclick={toggleNotifications}
            class="relative w-11 h-6 rounded-full transition-colors {settings.notifications ? 'bg-amber-700' : 'bg-neutral-300'}"
          >
            <span class="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform {settings.notifications ? 'translate-x-5' : 'translate-x-0'}"></span>
          </button>
        </div>
        <hr class="border-neutral-100" />
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <Eye class="w-4 h-4 text-neutral-500" />
            <div>
              <div class="text-sm font-medium text-neutral-700">Public Profile</div>
              <div class="text-xs text-neutral-500">Share your recipes with community</div>
            </div>
          </div>
          <button
            onclick={togglePublicProfile}
            class="relative w-11 h-6 rounded-full transition-colors {settings.publicProfile ? 'bg-amber-700' : 'bg-neutral-300'}"
          >
            <span class="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform {settings.publicProfile ? 'translate-x-5' : 'translate-x-0'}"></span>
          </button>
        </div>
      </div>
    </div>

    <!-- Account Actions -->
    <div class="p-4 bg-white border border-neutral-200 rounded-lg">
      {#each [[Mail, 'Email Settings'], [Lock, 'Privacy & Security'], [HelpCircle, 'Help & Support']] as [Icon, label], i}
        {#if i > 0}<hr class="my-1 border-neutral-100" />{/if}
        <button class="w-full flex items-center justify-between p-3 hover:bg-neutral-50 rounded-lg transition-colors">
          <div class="flex items-center gap-3">
            <svelte:component this={Icon} class="w-4 h-4 text-neutral-500" />
            <span class="text-sm text-neutral-700">{label}</span>
          </div>
          <ChevronRight class="w-4 h-4 text-neutral-400" />
        </button>
      {/each}
    </div>

    <!-- Sign Out -->
    <button class="w-full flex items-center justify-center gap-2 border border-red-200 text-red-600 hover:bg-red-50 hover:text-red-700 py-2.5 px-4 rounded-lg font-medium transition-colors">
      <LogOut class="w-4 h-4" /> Sign Out
    </button>

    <div class="text-center text-xs text-neutral-500 pb-4">
      TrueGrind v1.0.0<br />Made with ☕ by coffee enthusiasts
    </div>
  </div>
</PageLayout>
